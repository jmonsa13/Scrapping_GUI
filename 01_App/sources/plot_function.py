# Python project Dashboard for pricing
# Creado por: Juan Monsalvo
# ----------------------------------------------------------------------------------------------------------------------
# Libraries import
# ----------------------------------------------------------------------------------------------------------------------
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ----------------------------------------------------------------------------------------------------------------------
# Configuration and Global Variables
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Function Definition
# ----------------------------------------------------------------------------------------------------------------------
def plot_price_history(df, group, title, orient_h=False):
    """
    Función que crea el gráfico de historico de precio.
    :param df: data frame con los precios y la historia.
    :param group: Texto para agrupar o dibujar por referencia o familia.
    :param title: Título de la gráfica.
    :param orient_h: Default FALSE, para poner los legend de manera horizontal.
    :return: fig: Objeto de plotly para graficar externamente.
    """
    # Plotting line plot
    fig = px.line(data_frame=df, x="Fecha", y="Precio", color=group, line_group=group,
                  title=title,
                  width=1000, height=600,
                  labels={"Producto": "Product"},
                  template="seaborn")

    fig.update_traces(mode='lines+markers')
    fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"])

    fig.update_layout(
        xaxis=dict(
            rangeslider_visible=False,
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=3,
                         label="3m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(step="all")
                ])
            ),
            type="date"
        )
    )

    if orient_h is True:
        fig.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.13,  xanchor="left", x=0.01),
                          legend_title="Products")
    fig.update_xaxes(
        tickformatstops=[
            dict(dtickrange=["d1", "d30"], value="%b %d\n%Y"),
            dict(dtickrange=["d30", "d60"], value="%b '%y M"),
            dict(dtickrange=["d60", "d90"], value="%b '%y M"),
            dict(dtickrange=["M3", None], value="%Y Y")
        ]
    )
    fig.update_xaxes(showline=True, linewidth=0.5, linecolor='black')

    fig.update_yaxes(tickprefix="$", tickformat=",.2f")
    fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black')

    # Set x-axis and y-axis title
    fig['layout']['xaxis']['title'] = 'Date'
    fig['layout']['yaxis']['title'] = "Price in USD"

    return fig


def plot_price_history_index(df, group, mansfield_prod, title, orient_h=False):
    """
    Función que crea el gráfico de historico de precio.
    :param df: data frame con los precios y la historia.
    :param group: Texto para agrupar o dibujar por referencia o familia.
    :param mansfield_prod:
    :param title: Título de la gráfica.
    :param orient_h: Default FALSE, para poner los legend de manera horizontal.
    :return: fig: Objeto de plotly para graficar externamente.
    """

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Price over Time", "Price Positioning"),
                        column_widths=[0.7, 0.3],
                        )

    # Color Scheme definition
    line_color = {'Mansfield': 'rgba(23,55,95, 1)', 'American Standard': 'rgba(0, 0, 0, 1)',
                  'Gerber': 'rgba(1, 139, 250, 1)',
                  'Western Pottery': 'rgba(148, 103, 189, 1)'}
                  # 'rgba(140, 86, 75, 1)', 'rgba(227, 119, 194, 1)', 'rgba(127, 127, 127, 1)',
                  # 'rgba(188, 189, 34, 1)', 'rgba(23, 190, 207,1)', 'rgba(31, 119, 180, 1)'}

    # Plotting line plot
    product_order = []
    for product in df[group].unique():
        df_aux = df[df[group] == product]
        product_order.append(product)
        fig.add_trace(go.Scatter(x=df_aux['Fecha'], y=df_aux['Precio_factor'], name=product, legendgroup=product,
                                 line_color=line_color[df_aux['Fabricante'].iloc[0]], mode='lines+markers'),
                      row=1, col=1)

    # Calculating the price index
    df_index = df[df['Fecha'] == df['Fecha'].iloc[-1]][['Fecha', 'Fabricante',  group, 'Producto',
                                                        'Precio', 'Precio_factor']]
    mansfield_ref = df_index[df_index['Producto'] == mansfield_prod]['Precio_factor'].values

    df_index['Price_index'] = np.round(((mansfield_ref / df_index['Precio_factor']) * 100), 2)

    # Plotting scatter plot
    for product in product_order:
        df_aux = df_index[df_index[group] == product]
        fig.add_trace(go.Scatter(x=[mansfield_prod], y=df_aux['Price_index'],
                                 name=product, legendgroup=product,
                                 line_color=line_color[df_aux['Fabricante'].iloc[0]], mode='markers',
                                 showlegend=False),
                      row=1, col=2)

    # Title and template
    fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"], title_text=title, template="seaborn")

    # Range date button
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=3,
                         label="3m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(step="all")
                ])
            ),
            type="date"
        )
    )

    if orient_h is True:
        fig.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.13,  xanchor="left", x=0.01),
                          legend_title="Products")

    # Update xaxis, yaxis properties
    fig.update_xaxes(showline=True, linewidth=0.5, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black')

    # Configuration first plot
    fig.update_xaxes(rangeslider_visible=False, row=1, col=1)  # title_text="Date",
    fig.update_xaxes(
        tickformatstops=[
            dict(dtickrange=["d1", "d30"], value="%b %d\n%Y"),
            dict(dtickrange=["d30", "d60"], value="%b '%y M"),
            dict(dtickrange=["d60", "d90"], value="%b '%y M"),
            dict(dtickrange=["M3", None], value="%Y Y")
        ], row=1, col=1
    )
    fig.update_yaxes(title_text="Price in USD", tickprefix="$", tickformat=",.2f", row=1, col=1)

    # Configuration second plot
    fig.update_xaxes(row=1, col=2)  # title_text="Mansfield Product",
    fig.update_yaxes(title_text="% Price Index", ticksuffix="%", range=[40, 160], dtick=20, row=1, col=2)

    # Hover
    fig.update_traces(hovertemplate='%{y}', row=1, col=2)

    return fig


def plot_price_index_summary(df, comp_df, sku_list_mansfield, title, orient_h=False):
    """
    Función que crea el gráfico de historico de precio.
    :param df: data frame con los precios y la historia.
    :param title: Título de la gráfica.
    :param orient_h: Default FALSE, para poner los legend de manera horizontal.
    :return: fig: Objeto de plotly para graficar externamente.
    """
    # Initialization
    fig = go.Figure()

    # Color Scheme definition
    line_color = {'Mansfield': 'rgba(23,55,95, 1)', 'American Standard': 'rgba(0, 0, 0, 1)',
                  'Gerber': 'rgba(1, 139, 250, 1)',
                  'Western Pottery': 'rgba(148, 103, 189, 1)'}
                  # 'rgba(140, 86, 75, 1)', 'rgba(227, 119, 194, 1)', 'rgba(127, 127, 127, 1)',
                  # 'rgba(188, 189, 34, 1)', 'rgba(23, 190, 207,1)', 'rgba(31, 119, 180, 1)'}

    # Cont
    cont = 0
    flag = True

    # Products to visualize
    for i, sku_mansfield in enumerate(sku_list_mansfield):
        # sku competitors
        sku_comp = comp_df[comp_df['Homologo'] == sku_mansfield]['Sku']

        # Filter df
        df_comp = df[df['SKU_str'].isin(list(sku_comp))]

        # Calculating the price index
        df_info_price = df_comp[df_comp['Fecha'] == df_comp['Fecha'].iloc[-1]].copy()
        mansfield_ref = df_info_price[df_info_price['SKU_str'] == sku_mansfield]['Precio'].values
        mansfield_prod = df_info_price[df_info_price['SKU_str'] == sku_mansfield]['Producto_sku'].values

        df_info_price['Price_index'] = np.round(((mansfield_ref / df_info_price['Precio']) * 100), 2)

        for j, product in enumerate(df_info_price['Producto_sku'].unique()):
            df_aux = df_info_price[df_info_price['Producto_sku'] == product]

            fig.add_trace(go.Scatter(x=[i], y=df_aux['Price_index'],
                                     name=df_aux['Fabricante'].iloc[0], legendgroup=df_aux['Fabricante'].iloc[0],
                                     line_color=line_color[df_aux['Fabricante'].iloc[0]],
                                     mode='markers+text', marker_symbol='diamond', marker_size=8,
                                     text=f"{df_aux['Price_index'].iloc[0]}%", textposition="middle right",
                                     showlegend=flag))
            # Changing the xlabels
            fig.data[cont].x = mansfield_prod
            cont += 1
        flag = False

    # Title and template
    fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"], title_text=title, template="seaborn")

    if orient_h is True:
        fig.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.12, xanchor="left", x=0.01),
                          legend_title="Products")

    # Update xaxis, yaxis properties
    fig.update_xaxes(showline=True, linewidth=0.5, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black')

    # Configuration
    fig.update_yaxes(title_text="% Price Index", ticksuffix="%", range=[40, 140], dtick=10)
    fig.update_traces(hovertemplate='%{y}')

    return fig

def plot_price_history_summary(df, group, title, orient_h=False):
    """
    Función que crea el gráfico de historico de precio.
    :param df: data frame con los precios y la historia.
    :param group: Texto para agrupar o dibujar por referencia o familia.
    :param title: Título de la gráfica.
    :param orient_h: Default FALSE, para poner los legend de manera horizontal.
    :return: fig: Objeto de plotly para graficar externamente.
    """
    # Initialization
    fig = go.Figure()

    # Color Scheme definition
    line_color = {'Mansfield': 'rgba(23,55,95, 1)', 'American Standard': 'rgba(0, 0, 0, 1)',
                  'Gerber': 'rgba(1, 139, 250, 1)',
                  'Western Pottery': 'rgba(148, 103, 189, 1)'}
                  # 'rgba(140, 86, 75, 1)', 'rgba(227, 119, 194, 1)', 'rgba(127, 127, 127, 1)',
                  # 'rgba(188, 189, 34, 1)', 'rgba(23, 190, 207,1)', 'rgba(31, 119, 180, 1)'}

    for product in df[group].unique():
        df_aux = df[df[group] == product]
        fig.add_trace(go.Scatter(x=df_aux['Fecha'], y=df_aux['Precio'],
                                 name=df_aux[group].iloc[0], legendgroup=df_aux[group].iloc[0],
                                 line_color=line_color[df_aux['Fabricante'].iloc[0]], mode='lines+markers'))

    # Title and template
    fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"], title_text=title, template="seaborn")

    fig.update_layout(
        xaxis=dict(
            rangeslider_visible=False,
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=3,
                         label="3m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(step="all")
                ])
            ),
            type="date"
        )
    )

    if orient_h is True:
        fig.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.13,  xanchor="left", x=0.01),
                          legend_title="Products")

    # Update xaxis, yaxis properties
    fig.update_xaxes(title_text='Date', showline=True, linewidth=0.5, linecolor='black')
    fig.update_yaxes(title_text="Price in USD", showline=True, linewidth=0.5, linecolor='black')

    fig.update_yaxes(tickprefix="$", tickformat=",.2f")

    fig.update_xaxes(
        tickformatstops=[
            dict(dtickrange=["d1", "d30"], value="%b %d\n%Y"),
            dict(dtickrange=["d30", "d60"], value="%b '%y M"),
            dict(dtickrange=["d60", "d90"], value="%b '%y M"),
            dict(dtickrange=["M3", None], value="%Y Y")
        ]
    )
    return fig
