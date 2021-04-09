import datetime as dt
import os
import time
import numpy as np
import seaborn as sns
import yfinance as yf
import pandas as pd


pd.set_option('display.max_rows', 800)

x = os.listdir('../combined_dataframes/')
print (x)
x = sorted(x)
for i in x:
    j = i.replace('.csv', '')
    print (j)