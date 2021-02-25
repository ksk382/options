import datetime as dt
import os
import time
import numpy as np
import seaborn as sns
import yfinance as yf
from gather import load_ticker_list

today = dt.datetime.now()+ dt.timedelta(days = 1)
today_str = today.strftime("%Y-%m-%d")
data = yf.download(['COHR'], start='2021-01-20', end=today_str,
                    group_by="ticker")

print (data)
