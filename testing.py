import datetime as dt
import os
import time
import numpy as np
import seaborn as sns
import yfinance as yf
from gather import load_ticker_list
import pandas as pd

nope_dr = '../nope_dataframes/'
nope_names = [(nope_dr + i) for i in os.listdir(nope_dr) if i.endswith('_nope.csv')]
#nope_df = pd.read_csv(nope_name)
print (nope_names)

ticker_list = set(load_ticker_list())
print (len(ticker_list))

for i in nope_names:
    df = pd.read_csv(i, compression = 'gzip')
    t = set(df['ticker'].unique())
    ticker_list = ticker_list.difference(t)
    print (len(ticker_list))

ticker_list = list(ticker_list)
print (ticker_list)

ticker_df = pd.read_csv('IWV_holdings.csv')
print (len(ticker_df.index))
print (len(ticker_list))
d = ticker_df[~ticker_df['Ticker'].isin(ticker_list)]
print (d)
d = d.dropna()
d.to_csv('IWV_holdings.csv', index=False)


