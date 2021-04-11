import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import datetime as dt
import os
import time
import numpy as np
import seaborn as sns
import yfinance as yf
import pandas as pd
from api_auth import get_auth_headers
import requests
from cred_file import access_key, host
from api_calls import get_holdings, get_balance

d = get_holdings()
print (d)

e = get_balance()
print (e)




'''
most_recent_s_frame = '../stock_dataframes/2021-04-09_14.00.csv'
s_frame = pd.read_csv(most_recent_s_frame, compression='gzip')
s_frame['bid_ask_diff'] = s_frame['ask'] - s_frame['bid']
s_frame = s_frame[['symbol', 'bid_ask_diff', 'last']]
s_frame['pct_bid_ask_diff'] = s_frame['bid_ask_diff'] / s_frame['last']
print (s_frame.tail())
s_frame = s_frame.reset_index()
print (s_frame['pct_bid_ask_diff'].mean())
s_frame = s_frame.sort_values(by='pct_bid_ask_diff')
s_frame = s_frame.reset_index()
print (s_frame)
hist = s_frame.plot.scatter('index', 'pct_bid_ask_diff')
plt.show()
'''