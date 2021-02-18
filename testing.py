import datetime as dt
import os
import time
import numpy as np
import seaborn as sns
import yfinance as yf
from gather import load_ticker_list

ticker_list = load_ticker_list()
ticker_list = ticker_list

today = dt.datetime.now()+ dt.timedelta(days = 1)
today_str = today.strftime("%Y-%m-%d")
data = yf.download(ticker_list, start='2021-01-20', end=today_str,
                    group_by="ticker")

print (data)
data = data.T

data.to_csv('../ohlcv/main.csv', compression='gzip')
for ticker in ticker_list:
    df = data.loc[(ticker,),].T
    df['Date'] = df.index
    df.to_csv('../ohlcv/' + ticker + '.csv', compression = 'gzip', index=False)


