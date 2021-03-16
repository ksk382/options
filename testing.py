import datetime as dt
import os
import time
import numpy as np
import seaborn as sns
import yfinance as yf
import pandas as pd


today = dt.datetime.now()
# 253 trading days in a year
days_back = 60
DD = dt.timedelta(days=days_back)
earlier = today - DD
earlier_str = earlier.strftime("%Y-%m-%d")
end_str = today + dt.timedelta(days=1)

t = '^TNX'
data = yf.download(t, start=earlier_str, end=end_str,
                                group_by="ticker", interval='60m')


print (data)