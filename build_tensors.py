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



two_days_ago = '2021-02-01_21.57'
one_day_ago = '2021-02-02_15.30'
result_today = '2021-02-03_12.30'

def make_tensors(two_days_ago, one_day_ago, result_today):

       pd.set_option('display.max_rows', 800)
       pd.set_option('display.min_rows', 200)


       two_days_ago_file = f'../stock_dataframes/{two_days_ago}.csv'
       df1 = pd.read_csv(two_days_ago_file, compression = 'gzip')

       before_stock_file = f'../stock_dataframes/{one_day_ago}.csv'
       df2 = pd.read_csv(before_stock_file, compression = 'gzip')

       one_day_ago_nope_file = f'../nope_dataframes/{one_day_ago}_nope.csv'
       nope_df = pd.read_csv(one_day_ago_nope_file, compression = 'gzip')
       nope_df['symbol'] = nope_df['ticker']

       result_today_stock_file = f'../stock_dataframes/{result_today}.csv'
       mvmnt_df =  pd.read_csv(result_today_stock_file, compression = 'gzip')
       mvmnt_df['opn_z'] = mvmnt_df['opn']
       mvmnt_df = mvmnt_df[['symbol', 'opn_z']]

       df3 = pd.merge(df1, df2, on=['symbol'])
       df3 = pd.merge(df3, mvmnt_df, on='symbol')
       df3['label'] = (df3['opn_z'] - df3['cl_y']) / df3['cl_y']

       sp_500_df = pd.read_csv('sp500_ticker_list.csv')

       df3['sp'] = df3['symbol'].isin(sp_500_df['Ticker']) * 1

       # convert dates to datetime format
       df3['date_x'] = pd.to_datetime(df3['date_x'])
       df3['date_y'] = pd.to_datetime(df3['date_y'])

       # adding weekday
       df3['weekday_x'] = df3['date_x'].dt.dayofweek
       df3['weekday_y'] = df3['date_y'].dt.dayofweek

       print (df3)
       print (df3.loc[0])

       show_cols = []
       show_cols.append('label')
       show_cols.append('sp')

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

       out_name = f'../nope_dataframes/tensor_df_{one_day_ago}.csv'
       df5.to_csv(out_name, compression = 'gzip', index = False)
       print ('done')

def merge_tensors():
       dir_name = '../nope_dataframes/'
       x = os.listdir(dir_name)
       combined_tensor_df = pd.DataFrame([])
       for i in x:
              if i.startswith('tensor_df'):
                     j = dir_name + i
                     print (f'reading {j}')
                     df1 = pd.read_csv(j, compression = 'gzip')
                     print (df1.shape)
                     combined_tensor_df = combined_tensor_df.append(df1)
       print (f'final shape: {combined_tensor_df.shape}')
       out_name = dir_name + 'combined_tensor_df.csv'
       combined_tensor_df.to_csv(out_name, compression = 'gzip', index = False)


if __name__ == '__main__':
       x = '2021-02-02_15.30' # two evenings ago
       y = '2021-02-03_15.30' # one evening ago
       z = '2021-02-04_12.30' # anytime today that includes open price
       #make_tensors(x, y, z)
       merge_tensors()