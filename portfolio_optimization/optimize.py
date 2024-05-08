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


def efficient_frontier_plot(portfolios, min_vol_port, optimal_risky_port):
    # Hago el plot de la frontera eficiente
    fig, ax = plt.subplots()
    scatter = ax.scatter(
        portfolios["Volatility"], portfolios["Returns"], marker="o", s=10, alpha=0.3
    )
    ax.grid(True, alpha=0.5, linestyle="--")
    ax.set_xlabel("Volatility")
    ax.set_ylabel("Returns")
    ax.set_title("Portfolio Returns vs. Volatility")

    # Plot de los puntos para portfolio de varianza mínima y el óptimo
    ax.scatter(min_vol_port.iloc[1], min_vol_port.iloc[0], color="r", marker="*", s=500)
    ax.scatter(
        optimal_risky_port.iloc[1],
        optimal_risky_port.iloc[0],
        color="g",
        marker="*",
        s=500,
    )

    return fig


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

    # Hago el plot de la frontera eficiente
    fig = efficient_frontier_plot(portfolios, min_vol_port, optimal_risky_port)

    corr_matrix_html = corr_matrix.to_html()
    efficient_frontier = mpld3.fig_to_html(fig)

    # Hago un donut plot para min_vol_port y para optimal_risky_port
    fig_min = donut_plot(min_vol_port, "Min Volatility Portfolio")
    fig_opt = donut_plot(optimal_risky_port, "Optimal Risky Portfolio")

    return corr_matrix_html, efficient_frontier, fig_min, fig_opt
