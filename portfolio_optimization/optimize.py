import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import mpld3


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

    # Hago el plot de la frontera eficiente
    fig, ax = plt.subplots()
    scatter = ax.scatter(
        portfolios["Volatility"], portfolios["Returns"], marker="o", s=10, alpha=0.3
    )
    ax.grid(True, alpha=0.5, linestyle="--")
    ax.set_xlabel("Volatility")
    ax.set_ylabel("Returns")
    ax.set_title("Portfolio Returns vs. Volatility")

    corr_matrix_html = corr_matrix.to_html()
    efficient_frontier = mpld3.fig_to_html(fig)

    return corr_matrix_html, efficient_frontier
