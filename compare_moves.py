# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import requests
from cred_file import *
from io import StringIO
import xml.etree.ElementTree as ET
import pandas as pd
import datetime as dt
import os
import time
import numpy as np
import seaborn as sns


pd.set_option('display.max_rows', 800)

morning_nope_file = '../nope_dataframes/2021-02-02_09.30_nope.csv'
nope_df = pd.read_csv(morning_nope_file, compression = 'gzip')
nope_df['symbol'] = nope_df['ticker']
print (nope_df)

morning_stock_file = '../stock_dataframes/2021-02-02_09.30.csv'
morning_stock_df = pd.read_csv(morning_stock_file, compression = 'gzip')

later_stock_file = '../stock_dataframes/2021-02-02_16.19.csv'
stock_df = pd.read_csv(later_stock_file, compression = 'gzip')

morning_stock_df['morning'] = morning_stock_df['last']
morning_lasts = morning_stock_df[['symbol', 'morning']]
stock_df = pd.merge(stock_df, morning_lasts, on=['symbol'])
stock_df['change_from_morning'] = (stock_df['last'] - stock_df['morning']) / stock_df['morning']
df1 = pd.merge(stock_df, nope_df, on=['symbol'])
df1 = df1.dropna()
df1 = df1.round(3)
df1 = df1[df1['nope_metric'].abs() >.02]
df1['100_bucks'] = 100 + (100 * df1['change_from_morning'] * np.sign(df1['nope_metric']))
df1 = df1.sort_values(by='nope_metric', ascending = False)
df1 = df1[~df1.isin([np.nan, np.inf, -np.inf]).any(1)]
cols = ['symbol', 'last', 'morning', 'change_from_morning', 'nope_adv_21', 'nope_metric','100_bucks']
print (df1[cols])

print (df1['100_bucks'].sum())
print (len(df1.index) * 100)
roi = (df1['100_bucks'].sum() - (len(df1.index) * 100)) / (len(df1.index) * 100)
print (roi)

#df1.plot(x='Nope', y='change_from_morning', style='o')
#sns.regplot(df1['nope_metric'],df1['change_from_morning'])
#sns.regplot(df1['Nope'],df1['change_from_morning'])
#plt.show()


