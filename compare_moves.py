# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import os
import time
import numpy as np
import seaborn as sns


pd.set_option('display.max_rows', 800)

before = '2021-02-02_16.19'
after = '2021-02-03_09.30'

before_nope_file = f'../nope_dataframes/{before}_nope.csv'
nope_df = pd.read_csv(before_nope_file, compression = 'gzip')
nope_df['symbol'] = nope_df['ticker']
print (nope_df)

before_stock_file = f'../stock_dataframes/{before}.csv'
before_stock_df = pd.read_csv(before_stock_file, compression = 'gzip')

after_stock_file = f'../stock_dataframes/{after}.csv'
after_stock_df = pd.read_csv(after_stock_file, compression = 'gzip')

before_stock_df['before'] = before_stock_df['last']
before_lasts = before_stock_df[['symbol', 'before']]
after_stock_df = pd.merge(after_stock_df, before_lasts, on=['symbol'])

after_stock_df['change_from_before'] = (after_stock_df['last'] - after_stock_df['before']) / after_stock_df['before']
df1 = pd.merge(after_stock_df, nope_df, on=['symbol'])
df1 = df1.dropna()
df1 = df1[~df1.isin([np.nan, np.inf, -np.inf]).any(1)]
#df1 = df1.round(4)
#df1 = df1[df1['nope_metric'].abs() >.02]
df1['100_bucks'] = 100 + (100 * df1['change_from_before'] * np.sign(df1['nope_metric']))

var = 'nope_metric'
s = df1[var].mad()
print ('mad:', s)
#s = df1[dep_var].mean() + df1[dep_var].std()
#df1 = df1[df1[dep_var] > s]
df1 = df1[df1['nope_metric'].abs() > .02]
df1 = df1.sort_values(by=var, ascending = False)
df1 = df1[~df1.isin([np.nan, np.inf, -np.inf]).any(1)]


cols = ['symbol', 'last', 'before', 'change_from_before', 'nope_adv_21', 'nope_metric','100_bucks']
print (df1[cols])

print (f'investment: {(len(df1.index) * 100)}')
print (f'return: {(df1["100_bucks"].sum())}')
roi = (df1['100_bucks'].sum() - (len(df1.index) * 100)) / (len(df1.index) * 100)
print (roi)

#df1.plot(x='Nope', y='change_from_before', style='o')
sns.regplot(df1[var],df1['change_from_before'])
print (before, after)
plt.show()


