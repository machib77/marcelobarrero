import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


def optimize_portfolio(ticker_list, date_list):
    df = pd.DataFrame()
    for ticker in ticker_list:
        stock_data = yf.download(ticker, start=date_list[0], end=date_list[1])
        df[ticker] = stock_data["Adj Close"]
    df = df.dropna()
    cov_matrix = df.pct_change().apply(lambda x: np.log(1 + x)).cov()
    corr_matrix = df.pct_change().apply(lambda x: np.log(1 + x)).corr()
    return corr_matrix
