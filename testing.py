import datetime as dt
import os
import time
import numpy as np
import seaborn as sns
import yfinance as yf
import pandas as pd


pd.set_option('display.max_rows', 800)

label_date = '2021-04-01'

df = pd.read_csv('../ohlcv/ohlcv.csv', compression='gzip')
df = df[['symbol', 'date', 'close', 'high', 'low', 'open', 'volume', 'id', 'key',
       'subkey', 'updated', 'changeOverTime', 'marketChangeOverTime',
       'uOpen', 'uClose', 'uHigh', 'uLow', 'uVolume', 'fOpen', 'fClose',
       'fHigh', 'fLow', 'fVolume', 'label', 'change', 'changePercent']]
print (df)
df = df.drop_duplicates(subset=['symbol', 'date'], keep='first')

df.to_csv('../ohlcv/ohlcv.csv', compression='gzip', index=False)