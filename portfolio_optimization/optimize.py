import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


def get_prices(ticker_list, date_list):
    data = pd.DataFrame()
    for ticker in ticker_list:
        stock_data = yf.download(ticker, start=date_list[0], end=date_list[1])
        data[ticker] = stock_data["Adj Close"]
    data = data.dropna()
    return data.head()
