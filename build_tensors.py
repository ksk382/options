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

def munge(df1, df2, nope_df, sp_500_df):

       df3 = pd.merge(df1, df2, on=['symbol'])
       df3['sp'] = df3['symbol'].isin(sp_500_df['Ticker']) * 1

       # convert dates to datetime format
       df3['date_x'] = pd.to_datetime(df3['date_x'])
       df3['date_y'] = pd.to_datetime(df3['date_y'])

       # adding weekday
       df3['weekday_x'] = df3['date_x'].dt.dayofweek
       df3['weekday_y'] = df3['date_y'].dt.dayofweek
       show_cols = []
       show_cols.append('sp')
       show_cols.append('weekday_x')
       show_cols.append('weekday_y')

       day_chgs = ['opn','hi','lo', 'last', 'vl', 'vwap']
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
              df3[j] = (df3['last_y'] - df3[y]) / df3[y]

       volume_stretch = ['adv_21','adv_30','adv_90']
       for i in volume_stretch:
              y = i + '_y'
              j = i + '_stretch'
              show_cols.append(j)
              df3[j] = (df3['vl_y'] - df3[y]) / df3[y]

       show_cols = show_cols + ['sho_y']
       show_cols.append('symbol')
       show_cols.append('last_y')

       # shrinking down and merging dataframes
       df3 = df3[show_cols]
       df3 = df3[~df3.isin([np.nan, np.inf, -np.inf]).any(1)]
       df3['sho_y'] = pd.to_numeric(df3['sho_y'])
       df4 = pd.merge(df3, nope_df, on='symbol')
       df4.pop('ticker')
       df4['delta_over_sho'] = df4['net_delta'] / df4['sho_y']
       df4['gamma_over_sho'] = df4['net_gamma'] / df4['sho_y']
       df4.pop('net_delta')
       df4.pop('net_gamma')

       return df4

def make_training_tensors(df1, df2, df_future, nope_df, sp_500_df):

       mvmnt_df = df_future
       mvmnt_df['opn_z'] = mvmnt_df['opn']
       mvmnt_df = mvmnt_df[['symbol', 'opn_z']]

       df4 = munge(df1,df2,nope_df,sp_500_df)
       df5 = pd.merge(df4, mvmnt_df, on='symbol')
       df5['mvmnt'] = (df5['opn_z'] - df5['last_y']) / df5['last_y']
       df5.pop('opn_z')
       df5 = df5[~df5.isin([np.nan, np.inf, -np.inf]).any(1)]

       df2_date = df2['date'].head(1).item() + '_15.30'
       out_name = f'../nope_dataframes/tensor_df_set_{df2_date}.csv'
       df5.to_csv(out_name, compression = 'gzip', index = False)
       print ('done')
       return

def merge_tensors():
       dir_name = '../nope_dataframes/'
       x = os.listdir(dir_name)
       combined_tensor_df = pd.DataFrame([])
       for i in x:
              if i.startswith('tensor_df_set_'):
                     j = dir_name + i
                     print (f'reading {j}')
                     df1 = pd.read_csv(j, compression = 'gzip')
                     print (df1.shape)
                     combined_tensor_df = combined_tensor_df.append(df1)
       print (f'final shape: {combined_tensor_df.shape}')
       out_name = dir_name + 'combined_tensor_df.csv'
       combined_tensor_df.to_csv(out_name, compression = 'gzip', index = False)
       return

def make_rec_tensors(df1, df2, nope_df, sp_500_df):

       df3 = munge(df1,df2,nope_df,sp_500_df)
       df3 = df3[~df3.isin([np.nan, np.inf, -np.inf]).any(1)]
       df3['mvmnt'] = 0
       df5 = df3

       df5 = df5[~df5.isin([np.nan, np.inf, -np.inf]).any(1)]
       df5['mvmnt'] = 0
       # out_name = f'../nope_dataframes/tensor_df_{one_day_ago}_{ticker}.csv'
       # print (f'writing to {out_name}')
       # df5.to_csv(out_name, compression='gzip', index=False)
       return df5

def produce_training_data():
       all_dates = [
              '2021-02-01_15.30',
              '2021-02-02_15.30',
              '2021-02-03_15.30',
              '2021-02-04_15.30',
              '2021-02-05_09.30'
       ]

       for d in range(0, len(all_dates[:-2])):
              x = all_dates[d]
              y = all_dates[d + 1]
              z = all_dates[d + 2]
              print(x)
              print(y)
              print(z)

              two_days_ago_file = f'../stock_dataframes/{x}.csv'
              df1 = pd.read_csv(two_days_ago_file, compression='gzip')

              before_stock_file = f'../stock_dataframes/{y}.csv'
              df2 = pd.read_csv(before_stock_file, compression='gzip')

              result_today_stock_file = f'../stock_dataframes/{z}.csv'
              df_future = pd.read_csv(result_today_stock_file, compression='gzip')

              one_day_ago_nope_file = f'../nope_dataframes/{y}_nope.csv'
              nope_df = pd.read_csv(one_day_ago_nope_file, compression='gzip')
              nope_df['symbol'] = nope_df['ticker']

              sp_500_df = pd.read_csv('sp500_ticker_list.csv', compression='gzip')

              make_training_tensors(df1, df2, df_future, nope_df, sp_500_df)
              print('\n\n')

       return


if __name__ == '__main__':

       produce_training_data()
       merge_tensors()