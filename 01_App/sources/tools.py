# Python project Dashboard for pricing
# Creado por: Juan Monsalvo
# ----------------------------------------------------------------------------------------------------------------------
# Libraries import
# ----------------------------------------------------------------------------------------------------------------------
import math
import numpy as np
import urllib.request
import streamlit as st

from PIL import Image

# ----------------------------------------------------------------------------------------------------------------------
# Configuration and Global Variables
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Function Definition
# ----------------------------------------------------------------------------------------------------------------------
def url_image_capture(url):
    """
    Function for downloading the image contained on the URL. This function take into account empty URL and empty space
    between characters.
    """
    # Requesting the image | Download image from URL if possible
    try:
        if math.isnan(url):
            image = Image.open('images/Empty.png')
    except:
        url_image = url.replace(" ", "%20")  # Replacing whitespace

        # Introducing header to avoid error 404
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        try:
            urllib.request.urlretrieve(url_image, "images/image_product.png")
            # Loading image
            image = Image.open('images/image_product.png')
        except urllib.error.URLError as e:
            print(e.__dict__)
            # Loading image
            image = Image.open('images/Empty.png')

    return image


def producto_info_multiplier(df_product):
    """
    Function for plotting the information related to a single product
    """
    # Requesting the image | Download image from URL if possible
    image = url_image_capture(df_product["Image_url"].iloc[-1])

    # Title and image
    st.markdown(f'**{df_product["Producto"].iloc[-1]}**')
    image = image.resize((300, 300))
    with st.container():
        st.image(image)

    # Multiplier
    number = st.number_input('Insert the Multiplier Factor (%)', value=0, key=df_product["SKU"].iloc[-1])

    # Info detail
    with st.expander('Information'):
        st.markdown("* {} ({})".format(df_product["Producto"].iloc[-1],
                                       df_product["SKU"].iloc[-1])
                    )
        st.markdown("* Original price: ${:,} {}".format(
            df_product["Precio"].iloc[-1],
            df_product["Moneda"].iloc[-1]).replace(',', '.')
                    )
        st.markdown("* Multiplier price: ${:,} {}".format(
            np.round(df_product["Precio"].iloc[-1] * ((number/100) + 1),2),
            df_product["Moneda"].iloc[-1]).replace(',', '.')
                    )
        st.markdown("* [Web page]({})".format(df_product["URL"].iloc[-1]))
        
    return number


def visual_info_multiplier(df_comp):
    """"

    """
    # Creation of the price factor
    df_comp["Precio_factor"] = df_comp["Precio"]

    # Filtering out the Mansfield product
    df_comp_aux = df_comp[df_comp['Fabricante'] != 'Mansfield']

    # Conditional for total quantities of products
    if len(df_comp['Producto_sku'].unique()) == 3:
        p1, p2, p3 = st.columns(3)

        # Mansfield information
        with p1:
            multi_factor = producto_info_multiplier(df_comp[df_comp['Fabricante'] == 'Mansfield'])
            df_comp.loc[df_comp['Fabricante'] == 'Mansfield', 'Precio_factor'] *= ((multi_factor/100) + 1)

        # Product 1
        df_comp_product = df_comp[df_comp['Producto_sku'] == df_comp_aux['Producto_sku'].unique()[0]]
        with p2:
            multi_factor = producto_info_multiplier(df_comp_product)
            df_comp.loc[df_comp['Producto_sku'] == df_comp_aux['Producto_sku'].unique()[0], 'Precio_factor'] \
                *= ((multi_factor/100) + 1)

        # Product 2
        df_comp_product = df_comp[df_comp['Producto_sku'] == df_comp_aux['Producto_sku'].unique()[1]]
        with p3:
            multi_factor = producto_info_multiplier(df_comp_product)
            df_comp.loc[df_comp['Producto_sku'] == df_comp_aux['Producto_sku'].unique()[1], 'Precio_factor'] \
                *= ((multi_factor/100) + 1)

    elif len(df_comp['Producto_sku'].unique()) == 2:
        p1, p2 = st.columns(2)

        # Mansfield information
        with p1:
            multi_factor = producto_info_multiplier(df_comp[df_comp['Fabricante'] == 'Mansfield'])
            df_comp.loc[df_comp['Fabricante'] == 'Mansfield', 'Precio_factor'] *= ((multi_factor / 100) + 1)

        # Product 1
        df_comp_product = df_comp[df_comp['Producto_sku'] == df_comp_aux['Producto_sku'].unique()[0]]
        with p2:
            multi_factor = producto_info_multiplier(df_comp_product)
            df_comp.loc[df_comp['Producto_sku'] == df_comp_aux['Producto_sku'].unique()[0], 'Precio_factor'] \
                *= ((multi_factor/100) + 1)

    elif len(df_comp['Producto_sku'].unique()) == 4:
        p1, p2, p3, p4 = st.columns(4)

        # Mansfield information
        with p1:
            multi_factor = producto_info_multiplier(df_comp[df_comp['Fabricante'] == 'Mansfield'])
            df_comp.loc[df_comp['Fabricante'] == 'Mansfield', 'Precio_factor'] *= ((multi_factor / 100) + 1)

        # Product 1
        df_comp_product = df_comp[df_comp['Producto_sku'] == df_comp_aux['Producto_sku'].unique()[0]]
        with p2:
            multi_factor = producto_info_multiplier(df_comp_product)
            df_comp.loc[df_comp['Producto_sku'] == df_comp_aux['Producto_sku'].unique()[0], 'Precio_factor'] \
                *= ((multi_factor/100) + 1)

        # Product 2
        df_comp_product = df_comp[df_comp['Producto_sku'] == df_comp_aux['Producto_sku'].unique()[1]]
        with p3:
            multi_factor = producto_info_multiplier(df_comp_product)
            df_comp.loc[df_comp['Producto_sku'] == df_comp_aux['Producto_sku'].unique()[1], 'Precio_factor'] \
                *= ((multi_factor/100) + 1)

        # Product 3
        df_comp_product = df_comp[df_comp['Producto_sku'] == df_comp_aux['Producto_sku'].unique()[2]]
        with p4:
            multi_factor = producto_info_multiplier(df_comp_product)
            df_comp.loc[df_comp['Producto_sku'] == df_comp_aux['Producto_sku'].unique()[2], 'Precio_factor'] \
                *= ((multi_factor/100) + 1)
    return df_comp
