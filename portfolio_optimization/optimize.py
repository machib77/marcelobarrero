import numpy as np
import pandas as pd
import yfinance as yf

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import mpld3
from matplotlib.patches import Circle


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
        data[symbol + " weight"] = [w[counter] for w in p_weights]

    portfolios = pd.DataFrame(data)

    # Portfolio eficiente de volatilidad mínima
    min_vol_port = portfolios.iloc[portfolios["Volatility"].idxmin()]  # type: ignore

    # Portfolio óptimo
    rf = 0.01  # Por mientras como ejemplo
    optimal_risky_port = portfolios.iloc[((portfolios["Returns"] - rf) / portfolios["Volatility"]).idxmax()]  # type: ignore

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

    corr_matrix_html = corr_matrix.to_html()
    efficient_frontier = mpld3.fig_to_html(fig)

    # Hago un donnut plot para min_vol_port y para optimal_risky_port
    fig_donuts, axes = plt.subplots(1, 2, figsize=(10, 5))

    min_vol_port_filtered = min_vol_port.drop(["Returns", "Volatility"])
    min_vol_labels = min_vol_port_filtered.index
    min_vol_sizes = min_vol_port_filtered.values
    axes[0].pie(min_vol_sizes, labels=min_vol_labels, autopct="%1.1f%%", startangle=90)
    axes[0].axis("equal")
    axes[0].set_title("Min Volatility Portfolio")
    axes[0].add_artist(Circle((0, 0), 0.7, color="white"))

    optimal_risky_port_filtered = optimal_risky_port.drop(["Returns", "Volatility"])
    opt_risky_labels = optimal_risky_port_filtered.index
    opt_risky_sizes = optimal_risky_port_filtered.values
    axes[1].pie(
        opt_risky_sizes, labels=opt_risky_labels, autopct="%1.1f%%", startangle=90
    )
    axes[1].axis("equal")
    axes[1].set_title("Optimal Risky Portfolio")
    axes[1].add_artist(Circle((0, 0), 0.7, color="white"))

    fig_donuts_html = mpld3.fig_to_html(fig_donuts)

    return corr_matrix_html, efficient_frontier, fig_donuts_html
