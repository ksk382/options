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
import yfinance as yf

def munge(df1, df2, nope_df, sp_500_df, etf_df, spy_df):

       df2_date = df2.loc[0, 'date']
       spy_df = spy_df[spy_df['Date'] == df2_date].head(1)
       spy_delta = (spy_df['Close'] - spy_df['Open']) / spy_df['Open']
       df2['spy_delta'] = spy_delta.item()
       df2['spy_delta'].round(4)

       df3 = pd.merge(df1, df2, on=['symbol'])
       df3['sp'] = df3['symbol'].isin(sp_500_df['Ticker']) * 1
       df3['etf'] = df3['symbol'].isin(etf_df['Ticker']) * 1

       # convert dates to datetime format
       df3['date_x'] = pd.to_datetime(df3['date_x'])
       df3['date_y'] = pd.to_datetime(df3['date_y'])

       # adding weekday
       df3['weekday_x'] = df3['date_x'].dt.dayofweek
       df3['weekday_y'] = df3['date_y'].dt.dayofweek
       show_cols = []
       show_cols.append('sp')
       show_cols.append('etf')
       show_cols.append('weekday_x')
       show_cols.append('weekday_y')
       show_cols.append('spy_delta')

       day_chgs = ['opn_s','hi_s','lo_s', 'cl_s', 'vl_s', 'vwap']
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
              df3[j] = (df3['cl_s_y'] - df3[y]) / df3[y]

       volume_stretch = ['adv_21','adv_30','adv_90']
       for i in volume_stretch:
              y = i + '_y'
              j = i + '_stretch'
              show_cols.append(j)
              df3[j] = (df3['vl_y'] - df3[y]) / df3[y]

       show_cols = show_cols + ['sho_y']
       show_cols.append('symbol')
       show_cols.append('name_y')
       show_cols.append('cl_s_y')
       show_cols.append('date_y')
       show_cols.append('beta_y')
       show_cols.append('volatility12_y')
       show_cols.append('yield_y')

       # shrinking down and merging dataframes
       df3 = df3[show_cols]
       df3 = df3[~df3.isin([np.nan, np.inf, -np.inf]).any(1)]
       df3['sho_y'] = pd.to_numeric(df3['sho_y'])
       df4 = pd.merge(df3, nope_df, on='symbol')
       df4.pop('ticker')
       df4['delta_over_sho'] = df4['net_idelta'] / df4['sho_y']
       df4['gamma_over_sho'] = df4['net_igamma'] / df4['sho_y']
       #df4.pop('net_delta')
       #df4.pop('net_gamma')

       return df4

def make_training_tensors(df1, df2, df_future, nope_df, sp_500_df, etf_df, spy_df):

       mvmnt_df = df_future
       mvmnt_df['opn_z'] = mvmnt_df['opn_s']
       mvmnt_df = mvmnt_df[['symbol', 'opn_z']]

       df4 = munge(df1,df2,nope_df,sp_500_df, etf_df, spy_df)
       df5 = pd.merge(df4, mvmnt_df, on='symbol')
       df5['mvmnt'] = (df5['opn_z'] - df5['cl_s_y']) / df5['cl_s_y']
       df5.pop('opn_z')
       df5 = df5[~df5.isin([np.nan, np.inf, -np.inf]).any(1)]

       df2_date = df2['date'].head(1).item() + '_15.30'
       out_name = f'../nope_dataframes/tensor_df_set_{df2_date}.csv'
       df5.to_csv(out_name, compression = 'gzip', index = False)
       print ('done')
       return

def make_rec_tensors(df1, df2, nope_df, sp_500_df, etf_df):

       # get a ohlcv prices for the S&P
       today = dt.datetime.now() + dt.timedelta(days=1)
       today_str = today.strftime("%Y-%m-%d")
       spy_df = yf.download('spy', start='2021-01-20', end=today_str,
                            group_by="ticker")
       spy_df['Date'] = spy_df.index

       df3 = munge(df1,df2,nope_df,sp_500_df, etf_df, spy_df)
       df3 = df3[~df3.isin([np.nan, np.inf, -np.inf]).any(1)]
       df3['mvmnt'] = 0
       df5 = df3

       df5 = df5[~df5.isin([np.nan, np.inf, -np.inf]).any(1)]
       df5['mvmnt'] = 0
       # out_name = f'../nope_dataframes/tensor_df_{one_day_ago}_{ticker}.csv'
       # print (f'writing to {out_name}')
       # df5.to_csv(out_name, compression='gzip', index=False)
       return df5

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


def produce_training_data(all_dates):

       # get a ohlcv prices for the S&P
       today = dt.datetime.now() + dt.timedelta(days=1)
       today_str = today.strftime("%Y-%m-%d")
       spy_df = yf.download('spy', start='2021-01-20', end=today_str,
                            group_by="ticker")
       spy_df['Date'] = spy_df.index

       for d in range(0, len(all_dates[:-2])):
              x = all_dates[d]
              y = all_dates[d + 1]
              z = all_dates[d + 2]
              print(x)
              print(y)
              print(z)

              two_days_ago_file = f'../stock_dataframes/{x}_synth.csv'
              df1 = pd.read_csv(two_days_ago_file, compression='gzip')

              before_stock_file = f'../stock_dataframes/{y}_synth.csv'
              df2 = pd.read_csv(before_stock_file, compression='gzip')

              #result_today_stock_file = f'../stock_dataframes/{z}_synth.csv'
              result_today_stock_file = f'../stock_dataframes/{z}_synth.csv'
              df_future = pd.read_csv(result_today_stock_file, compression='gzip')

              one_day_ago_nope_file = f'../nope_dataframes/{y}_nope.csv'
              nope_df = pd.read_csv(one_day_ago_nope_file, compression='gzip')
              nope_df['symbol'] = nope_df['ticker']

              sp_500_df = pd.read_csv('sp500_ticker_list.csv', compression='gzip')
              etf_df = pd.read_csv('etf_ticker_list.csv', compression = 'gzip')

              make_training_tensors(df1, df2, df_future, nope_df, sp_500_df, etf_df, spy_df)
              print('\n\n')

       return

def check_mvmnt_dist():
       pd.set_option('display.max_rows', 2000)
       pd.set_option('display.min_rows', 200)

       np.set_printoptions(precision=3, suppress=True)

       log_dir = '../ML_logs/'
       if not os.path.exists(log_dir):
              os.mkdir(log_dir)

       df_file = '../nope_dataframes/combined_tensor_df.csv'
       df = pd.read_csv(df_file, compression='gzip')

       df = df.apply(pd.to_numeric, errors='coerce')
       df = df.dropna(axis=1, how='all')

       sns.distplot(df[['mvmnt']], hist=False, rug=True)

       df = df.sort_values(by='mvmnt')
       print(df)

       x = input('Show plot? (y)\n')
       if x == 'y':
              plt.show()

if __name__ == '__main__':
       all_dates = [
              '2021-02-01_15.30',
              '2021-02-02_15.30',
              '2021-02-03_15.30',
              '2021-02-04_15.30',
              '2021-02-05_15.30',
              '2021-02-08_15.30',
              '2021-02-09_15.00',
              '2021-02-10_15.00',
              '2021-02-11_15.00',
              '2021-02-16_14.30',
              '2021-02-17_14.30',
              '2021-02-18_14.30',
              '2021-02-19_14.30',
              '2021-02-22_14.30',
              '2021-02-23_14.30'
       ]


       produce_training_data(all_dates)
       merge_tensors()
       check_mvmnt_dist()