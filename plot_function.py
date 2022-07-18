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
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
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


def plot_price_index(df, group, mansfield_prod, title, orient_h=False):
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
    line_color = ['rgba(255,127,0, 1)', 'rgba(44, 160, 44, 1)', 'rgba(214, 39, 40, 1)',
                  'rgba(148, 103, 189, 1)', 'rgba(140, 86, 75, 1)',
                  'rgba(227, 119, 194, 1)', 'rgba(127, 127, 127, 1)',
                  'rgba(188, 189, 34, 1)', 'rgba(23, 190, 207,1)', 'rgba(31, 119, 180, 1)']

    # Plotting line plot
    product_order = []
    for i, product in enumerate(df[group].unique()):
        df_aux = df[df[group] == product]
        product_order.append(product)
        fig.add_trace(go.Scatter(x=df_aux['Fecha'], y=df_aux['Precio'], name=product, legendgroup=product,
                                 line_color=line_color[i], mode='lines+markers'),
                      row=1, col=1)

    # Calculating the price index
    df_index = df[df['Fecha'] == df['Fecha'].iloc[-1]][['Fecha', group, 'Producto', 'Precio']]
    mansfield_ref = df_index[df_index['Producto'] == mansfield_prod]['Precio'].values

    df_index['Price_index'] = (((mansfield_ref - df_index['Precio']) / df_index['Precio']) * 100) + 100

    # Plotting scatter plot
    for i, product in enumerate(product_order):
        df_aux = df_index[df_index[group] == product]
        fig.add_trace(go.Scatter(x=[mansfield_prod], y=np.round(df_aux['Price_index'], 2),
                                 name=product, legendgroup=product,
                                 line_color=line_color[i], mode='markers',
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
        fig.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.12,  xanchor="left", x=0.01),
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
    fig.update_traces(hovertemplate='%{y}',
                      row=1, col=2)

    return fig
