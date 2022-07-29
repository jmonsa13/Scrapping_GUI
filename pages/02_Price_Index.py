# Python project Dashboard for pricing
# Creado por: Juan Monsalvo
# ----------------------------------------------------------------------------------------------------------------------
# Libraries import
# ----------------------------------------------------------------------------------------------------------------------
import urllib.request

import os
import math
import numpy as np
import pandas as pd

from PIL import Image
import streamlit as st
from st_aggrid import AgGrid

from plot_function import plot_price_history, plot_price_index

# ----------------------------------------------------------------------------------------------------------------------
# Function Definition
# ----------------------------------------------------------------------------------------------------------------------
def load_data(filename="Decorceramica_twopieces.csv"):
    """
    Función que carga el archivo csv guardado al conectar con la base de datos y devuelve un dataframe
    """
    df = pd.read_csv(filename)

    return df


# ----------------------------------------------------------------------------------------------------------------------
# Configuration and Global Variables
# ----------------------------------------------------------------------------------------------------------------------
# Loading the files
# Folder path definition
directory = '.\\XX_Data'

files_list = []
for path, _, files in os.walk(directory):
    for name in files:
        files_list.append(os.path.join(path, name))

# Empty data frame
df = pd.DataFrame()

# Loading the DF of each month in a unique DF
for file in files_list:
    df = pd.concat([df, load_data(filename=file)])

# Dropping duplicates in case the robot take two values by day
df.drop_duplicates(inplace=True)

# Creating a new product name combining the product name + sku
df['Producto_sku'] = ['_'.join(i) for i in zip(df['Producto'], df['SKU'].map(str))]

# String the SKU
df['SKU_str'] = df['SKU'].map(str)

# ----------------------------------------------------------------------------------------------------------------------
# Loading the Master Database
# Reading files with the directory for comparisons
comp_df = pd.read_excel('XX_Master_database/Productos Mansfield.xlsx')

# Organizing the SKU
comp_df['Homologo'] = comp_df['Homologo Mansfield'].map(str)
comp_df['Homologo'] = comp_df['Homologo'].apply(lambda x: x.strip())

# ----------------------------------------------------------------------------------------------------------------------
# Streamlit Setting
# ----------------------------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Price Monitoring",
                   initial_sidebar_state="collapsed",
                   page_icon="📈",
                   layout="wide")

st.title('💲General Summary - Price Monitoring')
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
st.header('1) Price Over Time')
st.subheader('Filters to apply')

# Layout
col1, col2, col3 = st.columns([1, 2, 2])
with col1:
    filt1 = st.radio("Select one option", ['Marketplace', 'Brand', 'SKU', 'Price Range'], 0)

# SKU filters
if filt1 == 'SKU':
    with col2:
        sku_filter = st.text_input('Which SKU wants to visualize?', '135010007')
        # Convert to number if possible
        if sku_filter.isdigit():
            sku_filter = int(sku_filter)
        df_filter = df[df["SKU"] == sku_filter]  # 4021.101N.020, N2420, 135010007

    if len(df_filter) == 0:
        st.error(f"SKU {sku_filter} not found in dataset")

# Marketplace, Brand selection and Price Range
else:
    with col2:
        # Filtering by marketplace
        if filt1 == 'Marketplace':
            market_brand_sel = st.selectbox("Which marketplace wants to visualize?", df["Market_Place"].unique(), 0)
            df_filter = df[df["Market_Place"] == market_brand_sel]

        # Filtering by brand
        elif filt1 == 'Brand':
            market_brand_sel = st.selectbox("Which brands wants to visualize?", df["Fabricante"].unique(), 0)
            df_filter = df[df["Fabricante"] == market_brand_sel]

        # Range price
        elif filt1 == 'Price Range':
            price_range = st.slider('Select a range of prices', df['Precio'].min(), 1000.0,
                                    (100.0, 200.0), step=1.0)

            # Filtering the price by the last data
            df_filter_aux = df[(df["Precio"] >= price_range[0]) & (df["Precio"] <= price_range[1]) &
                               (df["Fecha"] == df.iloc[-1]['Fecha'])]

            df_filter = df[df['Producto_sku'].isin(list(df_filter_aux['Producto_sku'].unique()))]

    with col3:
        # filtering by format
        market_brand_sel = st.selectbox("Which format wants to visualize?", ['All'] +
                                        list(df_filter["Tipo"].unique()))
        if market_brand_sel == 'All':
            pass
        else:
            df_filter = df_filter[df_filter["Tipo"] == market_brand_sel]

# ------------------------------------------------------------------------------------------------------------------
# Plotting line plot
if len(df_filter) == 0:
    pass
else:
    fig = plot_price_history(df=df_filter, group="Producto_sku", title="Price over Time")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Explore data"):
        AgGrid(df_filter[['Fecha', 'Producto_sku', 'Precio', 'Market_Place']],
               editable=False, sortable=True, filter=True, resizable=True, defaultWidth=5,
               fit_columns_on_grid_load=False, theme="streamlit",  # "light", "dark", "blue", "material"
               key="Toilet", reload_data=True,  # gridOptions=gridoptions,
               enable_enterprise_modules=True)

    # --------------------------------------------------------------------------------------------------------------
    # Information from the product
    st.subheader("Information about the Product")

    # Filtering by reference
    ref = st.selectbox("¿Which reference wants to see?", list(df_filter["Producto_sku"].unique()))
    product_ref = df_filter[df_filter["Producto_sku"] == ref]

    # Requesting the image | Download image from URL if possible
    try:
        if math.isnan(product_ref["Image_url"].iloc[-1]):
            image = Image.open('01_Ref_images/Empty.png')
    except:
        url_image = product_ref["Image_url"].iloc[-1].replace(" ", "%20")  # Replacing whitespace

        # Introducing header to avoid error 404
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        try:
            urllib.request.urlretrieve(url_image, "01_Ref_images/image_info.png")
            # Loading image
            image = Image.open('01_Ref_images/image_info.png')
        except urllib.error.URLError as e:
            print(e.__dict__)
            # Loading image
            image = Image.open('01_Ref_images/Empty.png')

    # Plot image
    st.image(image, caption='{} ({}) ${:,} {}'.format(product_ref["Producto"].iloc[-1],
                                                      product_ref["SKU"].iloc[-1],
                                                      product_ref["Precio"].iloc[-1],
                                                      product_ref["Moneda"].iloc[-1]).replace(',', '.'),
             width=300)

    # General information
    st.markdown("**The url of the product is:** {}".format(product_ref["URL"].iloc[-1]))

# ----------------------------------------------------------------------------------------------------------------------
st.header('2) Comparison Products Mansfield')

# Mansfield df
Mansfield_df = df[df["Fabricante"] == 'Mansfield']

cc1, cc2 = st.columns((1, 3))
# filtering by format
format_mansfield_sel = cc1.selectbox("Which format wants to compare?", ['All'] +
                                     list(Mansfield_df["Tipo"].unique()))
if format_mansfield_sel == 'All':
    pass
else:
    Mansfield_df = Mansfield_df[Mansfield_df["Tipo"] == format_mansfield_sel]

# Mansfield product to compare
mansfield_product_sel = cc1.selectbox("Which Mansfield product wants to compare?",
                                      Mansfield_df["Producto"].unique(), 0)

mansfield_product = Mansfield_df[Mansfield_df['Producto'] == mansfield_product_sel]
sku_mansfield = mansfield_product.iloc[-1]['SKU']

# Requesting the image
urllib.request.urlretrieve(mansfield_product["Image_url"].iloc[-1], "01_Ref_images/image_mansfield.png")
image = Image.open('01_Ref_images/image_mansfield.png')
cc1.image(image, caption='{} ({}) ${:,} {}'.format(mansfield_product["Producto"].iloc[-1],
                                                   mansfield_product["SKU"].iloc[-1],
                                                   mansfield_product["Precio"].iloc[-1],
                                                   mansfield_product["Moneda"].iloc[-1]).replace(',', '.'),
          width=300)

# General information
cc1.markdown("**The url of the product is:** {}".format(mansfield_product["URL"].iloc[-1]))

# Products to visualize
sku_comp = comp_df[comp_df['Homologo'] == str(sku_mansfield)]['Sku']

# Filter df
df_comp = df[df['SKU_str'].isin(list(sku_comp))]

# Plot price index
fig = plot_price_index(df=df_comp, group="Producto_sku", mansfield_prod=mansfield_product_sel,
                       title=f"Mansfield Price index for {mansfield_product_sel}", orient_h=True)
cc2.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------------------------------------------------------
# Price index summary and data explorer
st.markdown("""---""")

# Price index
df_info_price = df_comp[df_comp['Fecha'] == df_comp['Fecha'].iloc[-1]]
mansfield_ref = df_info_price[df_info_price['Producto'] == mansfield_product_sel]['Precio'].values
df_info_price['Price_index'] = np.round(((mansfield_ref / df_info_price['Precio']) * 100), 2)

# Calculating overall price index
overall_price_index = np.round((df_info_price['Price_index'].abs().sum() - 100) / (len(df_info_price) - 1), 2)

ccc1, ccc2 = st.columns((1, 3))
with ccc1:
    st.metric(label="Overall Price Index", value=f"{overall_price_index}%")

with ccc2:
    AgGrid(df_info_price[['Fecha', 'Market_Place', 'Linea', 'Producto', 'Precio', 'URL']],
           editable=True, sortable=True, filter=True, resizable=True, defaultWidth=5, height=140,
           fit_columns_on_grid_load=False, theme="streamlit",  # "light", "dark", "blue", "material"
           key="price_index", reload_data=True,  # gridOptions=gridoptions,
           enable_enterprise_modules=False)

