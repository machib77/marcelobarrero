import numpy as np
import pandas as pd
import yfinance as yf

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import mpld3
from matplotlib.patches import Circle

import plotly.express as px
import plotly.offline as pyo
import plotly.graph_objects as go


def efficient_frontier_plot(portfolios, min_vol_port, optimal_risky_port):
    # Hago el plot de la frontera eficiente

    fig = go.Figure()

    scatter_trace = go.Scatter(
        x=portfolios["Volatility"],
        y=portfolios["Returns"],
        mode="markers",
        marker=dict(color="rgba(228,209,149,0.5)", opacity=0.3),
        showlegend=False,
    )
    fig.add_trace(scatter_trace)

    min_vol_port_trace = go.Scatter(
        x=[min_vol_port.iloc[1]],
        y=[min_vol_port.iloc[0]],
        mode="markers",
        marker=dict(color="rgba(242,71,62,1)", size=15, symbol="star"),
        name="Minimum Volatility Portfolio",
    )

    optimal_risky_port_trace = go.Scatter(
        x=[optimal_risky_port.iloc[1]],
        y=[optimal_risky_port.iloc[0]],
        mode="markers",
        marker=dict(color="rgba(4,170,109,1)", size=15, symbol="star"),
        name="Optimal Risky Portfolio",
    )

    fig.add_trace(min_vol_port_trace)
    fig.add_trace(optimal_risky_port_trace)

    # Update layout
    fig.update_layout(
        title=dict(
            text="Portfolio Returns vs. Volatility",
            x=0.5,  # Center the title horizontally
            y=0.95,  # Adjust the vertical position of the title
            font=dict(
                color="white", size=18, family="Arial Black"
            ),  # Set font color, size, and family
        ),
        xaxis=dict(
            title="Volatility",
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(237,231,225,0.1)",
            titlefont=dict(color="white"),  # Set the x-axis title font color to white
            tickfont=dict(color="white"),
        ),
        yaxis=dict(
            title="Returns",
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(237,231,225,0.1)",
            titlefont=dict(color="white"),  # Set the x-axis title font color to white
            tickfont=dict(color="white"),
        ),
        legend=dict(
            orientation="h",
            x=0.25,  # Adjust the x position of the legend
            y=-0.2,  # Adjust the y position of the legend
            bgcolor="rgba(255,255,255,0.5)",  # Set a semi-transparent background
        ),
        plot_bgcolor="rgba(51,51,51,0.5)",  # Set the plot background to transparent
        paper_bgcolor="rgba(0,0,0,0)",
        autosize=True,
        margin=dict(l=10, r=10, t=70, b=50),
        height=700,
    )

    html_str = pyo.plot(fig, output_type="div", include_plotlyjs=False)

    return html_str


def donut_plot(portfolio, title):
    portfolio_filtered = portfolio.drop(["Returns", "Volatility"], axis="index")
    subtitle = f"Expected Return: {portfolio.Returns*100:.1f}%, Volatility: {portfolio.Volatility*100:.1f}%"
    labels = portfolio_filtered.index
    values = portfolio_filtered.values

    hover_template = "<b>Ticker</b>: %{label}<br>" + "<b>Weight</b>: %{value:.1f}%<br>"

    fig = px.pie(
        values=values,
        names=labels,
        hover_name=labels,
        title=title,
        hole=0.3,
    )

    fig.update_traces(hovertemplate=hover_template, values=[x * 100 for x in values])

    fig.update_layout(
        title={
            "text": title,
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        title_font_size=20,
        font_size=14,
        annotations=[
            dict(
                text=subtitle,
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=1.2,
                xanchor="center",
                yanchor="top",
            )
        ],
    )

    html_str = pyo.plot(fig, output_type="div", include_plotlyjs=False)

    return html_str


def optimize_portfolio(ticker_list, date_list):
    # Obtengo los datos de yahoo finance
    df = pd.DataFrame()
    for ticker in ticker_list:
        stock_data = yf.download(ticker, start=date_list[0], end=date_list[1])
        df[ticker] = stock_data["Adj Close"]
    df = df.dropna()

    # Calculo la matrix de carianza y de correlación
    cov_matrix = df.pct_change().apply(lambda x: np.log(1 + x)).cov()
    corr_matrix = df.pct_change().apply(lambda x: np.log(1 + x)).corr()

    # Retornos anualizados para compañías individuales
    ind_er = df.resample("YE").last().pct_change().mean()

    # Desviación estándar anualizada (250 trading days / year)
    ann_sd = (
        df.pct_change()
        .apply(lambda x: np.log(1 + x))
        .std()
        .apply(lambda x: x * np.sqrt(250))
    )

    # Simulo 10000 portfolios
    p_ret = []
    p_vol = []
    p_weights = []
    num_assets = len(df.columns)
    num_portfolios = 10000

    for portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights = weights / np.sum(weights)
        p_weights.append(weights)
        returns = np.dot(weights, ind_er)
        p_ret.append(returns)
        var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()
        sd = np.sqrt(var)
        ann_sd = sd * np.sqrt(250)
        p_vol.append(ann_sd)

    data = {"Returns": p_ret, "Volatility": p_vol}

    for counter, symbol in enumerate(df.columns.tolist()):
        data[symbol] = [w[counter] for w in p_weights]

    portfolios = pd.DataFrame(data)

    # Portfolio eficiente de volatilidad mínima
    min_vol_port = portfolios.iloc[portfolios["Volatility"].idxmin()]  # type: ignore

    # Portfolio óptimo
    rf = 0.01  # Por mientras como ejemplo
    optimal_risky_port = portfolios.iloc[((portfolios["Returns"] - rf) / portfolios["Volatility"]).idxmax()]  # type: ignore

    corr_matrix_html = corr_matrix.to_html()

    # Hago el plot de la frontera eficiente
    efficient_frontier = efficient_frontier_plot(
        portfolios, min_vol_port, optimal_risky_port
    )

    # Hago un donut plot para min_vol_port y para optimal_risky_port
    fig_min = donut_plot(min_vol_port, "Min Volatility Portfolio")
    fig_opt = donut_plot(optimal_risky_port, "Optimal Risky Portfolio")

    return corr_matrix_html, efficient_frontier, fig_min, fig_opt
