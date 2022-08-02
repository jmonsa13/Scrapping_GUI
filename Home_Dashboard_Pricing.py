# Python project Dashboard for pricing
# Creado por: Juan Monsalvo
# ----------------------------------------------------------------------------------------------------------------------
# Libraries import
# ----------------------------------------------------------------------------------------------------------------------
import urllib.request

import os
import numpy as np
import pandas as pd

from PIL import Image
import streamlit as st
from st_aggrid import AgGrid

from plot_function import plot_price_history_summary, plot_price_index_summary


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
directory = './XX_Data'

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
# Mansfield df Summary products
sku_list_mansfield = ['130010007', '135010007', '137210040', '160010007', '384010000', '386010000']

Mansfield_df = df[df["Fabricante"] == 'Mansfield']
Mansfield_df = Mansfield_df[Mansfield_df['SKU_str'].isin(sku_list_mansfield)]

# ----------------------------------------------------------------------------------------------------------------------
# Streamlit Setting
# ----------------------------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Price Monitoring",
                   initial_sidebar_state="collapsed",
                   page_icon="📈",
                   layout="wide")

st.title('General Summary - Price Monitoring')
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
st.header('Mansfield Price Index Summary')

# # Plot price index summary
fig = plot_price_index_summary(df=df, comp_df=comp_df, sku_list_mansfield= sku_list_mansfield,
                               title=f"Mansfield Price Index", orient_h=True)
st.plotly_chart(fig, use_container_width=True)


st.subheader('Price Analysis Detailed')
c1, c2 = st.columns((1, 3))
# Mansfield product to compare
mansfield_product_sel = c1.selectbox("Which Mansfield product wants to compare?", Mansfield_df["Producto"].unique(), 0)

mansfield_product = Mansfield_df[Mansfield_df['Producto'] == mansfield_product_sel]
sku_mansfield = mansfield_product.iloc[-1]['SKU']

# Requesting the image
urllib.request.urlretrieve(mansfield_product["Image_url"].iloc[-1], "01_Ref_images/image_mansfield.png")
image = Image.open('01_Ref_images/image_mansfield.png')
c1.image(image, caption='{} ({}) ${:,} {}'.format(mansfield_product["Producto"].iloc[-1],
                                                  mansfield_product["SKU"].iloc[-1],
                                                  mansfield_product["Precio"].iloc[-1],
                                                  mansfield_product["Moneda"].iloc[-1]).replace(',', '.'),
         width=300)

# General information
c1.markdown("**The url of the product is:** {}".format(mansfield_product["URL"].iloc[-1]))

# Products to visualize
sku_comp = comp_df[comp_df['Homologo'] == str(sku_mansfield)]['Sku']

# Filter df
df_comp = df[df['SKU_str'].isin(list(sku_comp))]

# Plot price history
fig = plot_price_history_summary(df=df_comp, group="Producto_sku",
                                 title=f"Mansfield Price index for {mansfield_product_sel}",
                                 orient_h=True)

fig.update_layout(height=420)
c2.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------------------------------------------------------
# Price index summary and data explorer
st.markdown("""---""")

# Price index
df_info_price = df_comp[df_comp['Fecha'] == df_comp['Fecha'].iloc[-1]].copy()
mansfield_ref = df_info_price[df_info_price['Producto'] == mansfield_product_sel]['Precio'].values
df_info_price['Price_index'] = np.round(((mansfield_ref / df_info_price['Precio']) * 100), 2)

# Calculating overall price index
overall_price_index = np.round((df_info_price['Price_index'].abs().sum() - 100) / (len(df_info_price) - 1), 2)

cc1, cc2 = st.columns((1, 8))
with cc1:
    st.metric(label="Overall Price Index", value=f"{overall_price_index}%")

with cc2:
    AgGrid(df_info_price[['Fecha', 'Market_Place', 'Linea', 'Producto', 'Precio', 'Price_index', 'URL']],
           editable=True, sortable=True, filter=True, resizable=True, defaultWidth=5, height=140,
           fit_columns_on_grid_load=False, theme="streamlit",  # "light", "dark", "blue", "material"
           key="price_index", reload_data=True,  # gridOptions=gridoptions,
           enable_enterprise_modules=False)
