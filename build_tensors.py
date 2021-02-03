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


def merge_stock_with_nope(before, after):

       before_nope_file = f'../nope_dataframes/{before}_nope.csv'
       nope_df = pd.read_csv(before_nope_file, compression = 'gzip')
       nope_df['symbol'] = nope_df['ticker']
       before_stock_file = f'../stock_dataframes/{before}.csv'
       df = pd.read_csv(before_stock_file, compression = 'gzip')

       after_stock_file = f'../stock_dataframes/{after}.csv'
       after_stock_df = pd.read_csv(after_stock_file, compression = 'gzip')
       df['before'] = df['last']
       before_lasts = df[['symbol', 'before']]
       after_stock_df = pd.merge(after_stock_df, before_lasts, on=['symbol'])
       after_stock_df['change_from_before'] = (after_stock_df['last'] - after_stock_df['before']) / after_stock_df['before']
       df = pd.merge(after_stock_df, nope_df, on=['symbol'])
       return df

pd.set_option('display.max_rows', 800)
pd.set_option('display.min_rows', 200)


before = '2021-02-01_21.57'
before_stock_file = f'../stock_dataframes/{before}.csv'
df1 = pd.read_csv(before_stock_file, compression = 'gzip')

before = '2021-02-02_16.19'
after = '2021-02-03_09.30'
before_stock_file = f'../stock_dataframes/{before}.csv'
df2 = pd.read_csv(before_stock_file, compression = 'gzip')

before_nope_file = f'../nope_dataframes/{before}_nope.csv'
nope_df = pd.read_csv(before_nope_file, compression = 'gzip')
nope_df['symbol'] = nope_df['ticker']

after_stock_file = f'../stock_dataframes/{after}.csv'
mvmnt_df =  pd.read_csv(after_stock_file, compression = 'gzip')
mvmnt_df['tmmrw_last'] = mvmnt_df['last']
mvmnt_df = mvmnt_df[['symbol', 'tmmrw_last']]

df3 = pd.merge(df1, df2, on=['symbol'])
df3 = pd.merge(df3, mvmnt_df, on='symbol')
df3['label'] = (df3['tmmrw_last'] - df3['cl_y']) / df3['cl_y']

show_cols = []
show_cols.append('label')

day_chgs = ['opn','hi','lo','cl', 'vl', 'vwap']
for i in day_chgs:
       x = i + '_x'
       y = i + '_y'
       j = i + '_pctchg_1d'
       show_cols.append(j)
       df3[j] = (df3[y] - df3[x]) / df3[x]

price_stretch = ['adp_100','adp_200','adp_50','wk52hi','wk52lo']
for i in price_stretch:
       y = i + '_y'
       j = i + '_stretch'
       show_cols.append(j)
       df3[j] = (df3['cl_y'] - df3[y]) / df3[y]

volume_stretch = ['adv_21','adv_30','adv_90']
for i in volume_stretch:
       y = i + '_y'
       j = i + '_stretch'
       show_cols.append(j)
       df3[j] = (df3['vl_y'] - df3[y]) / df3[y]

df3 = df3[~df3.isin([np.nan, np.inf, -np.inf]).any(1)]

show_cols = show_cols + ['sho_y']
df3['sho_y'] = pd.to_numeric(df3['sho_y'])

show_cols.append('symbol')

#shrinking down and merging dataframes
df3 = df3[show_cols]
df4 = pd.merge(df3, nope_df, on='symbol')
df4['delta_over_sho'] = df4['net_delta'] / df4['sho_y']
df4['gamma_over_sho'] = df4['net_gamma'] / df4['sho_y']

df4.pop('net_delta')
df4.pop('net_gamma')
df4.pop('ticker')
print (df4)
print (df4.columns)
df5 = df4

df5 = df5[~df5.isin([np.nan, np.inf, -np.inf]).any(1)]

out_name = f'../nope_dataframes/tensor_df_{before}.csv'
df5.to_csv(out_name, compression = 'gzip', index = False)
print ('done')