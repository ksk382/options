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

x = df[df['date'] == '2021-04-06']
print (x)
print (x.shape)