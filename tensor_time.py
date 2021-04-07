# -*- coding: utf-8 -*-
from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())
import pandas as pd
import os
import numpy as np
from create_combined_dfs import latest_file
import sys

pd.set_option('display.max_rows', 800)


def munge(df1, df2, quote_df):
    df3 = pd.merge(df1, df2, on=['symbol'])
    df3 = pd.merge(df3, quote_df, on=['symbol'])

    # convert dates to datetime format
    df3['df_date_x'] = pd.to_datetime(df3['df_date_x'])
    df3['df_date_y'] = pd.to_datetime(df3['df_date_y'])

    # adding weekday
    df3['weekday_x'] = df3['df_date_x'].dt.dayofweek
    df3['weekday_y'] = df3['df_date_y'].dt.dayofweek

    show_cols = []

    # add the columns that are not relative to any other
    s = ['symbol',
         'latestPrice',
         'df_date_y',
         'df_date_x',
         'sp_y',
         'etf_y',
         'weekday_x',
         'weekday_y',
         'beta_x_y',
         'beta_y_y',
         'volatility12_y',
         'yield_y',
         'marketcap_y',
         'employees_y',
         'ttmEPS_y',
         'ttmDividendRate_y',
         'dividendYield_y',
         'peRatio_y',
         'maxChangePercent_y',
         'year5ChangePercent_y',
         'year2ChangePercent_y',
         'year1ChangePercent_y',
         'ytdChangePercent_y',
         'month6ChangePercent_y',
         'month3ChangePercent_y',
         'month1ChangePercent_y',
         'day30ChangePercent_y',
         'day5ChangePercent_y',
         'sho_y',
         'nope_metric_y',
         'nope_adv_21_y',
         'net_idelta_y',
         'net_igamma_y',
         'noge_y',
         'noge_21_y',
         'mw_idelta_y',
         'mw_igamma_y',
         'mw_itheta_y',
         'mw_ivega_y',
         'iexVolume',
         'latestVolume']

    for i in s:
        show_cols.append(i)

    # add in relative values
    day_chgs = ['opn', 'hi', 'lo', 'cl', 'vl', 'vwap']
    for i in day_chgs:
        x = i + '_x'
        y = i + '_y'
        j = i + '_pctchg_1d'
        df3[j] = (df3[y] - df3[x]) / df3[x]
        show_cols.append(j)

    price_stretch = ['adp_100', 'adp_200', 'adp_50', 'wk52hi', 'wk52lo']
    for i in price_stretch:
        y = i + '_y'
        j = i + '_stretch'
        show_cols.append(j)
        df3[j] = (df3['latestPrice'] - df3[y]) / df3[y]

    volume_stretch = ['adv_21', 'adv_30', 'adv_90']
    for i in volume_stretch:
        y = i + '_y'
        j = i + '_stretch'
        show_cols.append(j)
        df3[j] = (df3['vl_y'] - df3[y]) / df3[y]

    df3 = df3[show_cols]
    df3 = df3[~df3.isin([np.nan, np.inf, -np.inf]).any(1)]
    df3 = df3.drop_duplicates()
    return df3

def label_the_tensors(df3, z_date):
    '''
    :param df3: the already munged data (constructed tensors)
    :param z_date: today i.e. this morning
    :return: df4, which is a set of tensors labeled with price movement overnight
    '''
    '''
    
    # this only works for older data where ohlcv exists. you won't call ohlcv mid-market 
    # if it needs to be really accurate though maybe the training data should be 
    # built with a two day lag so you can label it with ohlcv?
    '''

    ohlcv = pd.read_csv('../ohlcv/ohlcv.csv', compression='gzip')
    label_df = ohlcv[ohlcv['date'] == z_date][['symbol', 'open', 'date']]
    label_df.columns = ['symbol', 'tmrw_opn', 'z_date']
    label_df = label_df.sort_values(by='symbol')


    # this is if you want to do training data asap, but it relies on IEX open prices
    '''
    quote_dir = '../quote_dataframes/'
    x = os.listdir(quote_dir)
    z_file_list = [(quote_dir + i) for i in x if i.startswith(z_date)]
    fname = min(z_file_list, key=os.path.getctime)
    quote_df = pd.read_csv(fname, compression='gzip')
    quote_df['datetime'] = pd.to_datetime(quote_df['lastTradeTime'],unit='ms')
    quote_df['datetime'] = quote_df['datetime'].dt.tz_localize('utc').dt.tz_convert('US/Eastern').dt.round('1s')
    quote_df['date] = quote_df['datetime'].dt.date
    label_df = quote_df[['symbol', 'latestPrice', 'datetime']]
    label_df.columns = ['symbol', 'tmrw_opn', 'datetime']
    label_df = label_df.sort_values(by='symbol')'''

    print (f'label_df shape: {label_df}')
    if label_df.empty:
        print (f'empty label df. ending {Path(__file__).resolve()}')
        sys.exit()

    df4 = pd.merge(df3, label_df, on='symbol')
    df4['mvmnt'] = (df4['tmrw_opn'] - df4['latestPrice']) / df4['latestPrice']
    return df4

def make_labeled_tensors(x_date, y_date, z_date):
    df1 = pd.read_csv(f'../combined_dataframes/{x_date}.csv', compression='gzip')
    df2 = pd.read_csv(f'../combined_dataframes/{y_date}.csv', compression='gzip')
    quote_df_name = latest_file('../quote_dataframes/', y_date)
    quote_df = pd.read_csv(quote_df_name, compression='gzip')

    print (f'initial_shapes--    df1: {df1.shape}    df2: {df2.shape}   quote_df: {quote_df.shape}')

    df3 = munge(df1, df2, quote_df)
    df4 = label_the_tensors(df3, z_date)
    df4 = df4[~df4.isin([np.nan, np.inf, -np.inf]).any(1)]
    out_name = f'../ML_content/tensor_df_set_{y_date}.csv'
    df4.to_csv(out_name, compression='gzip', index=False)
    return df4

def make_training_tensors(x_date, y_date, z_date):
    dir_name = '../ML_content/'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    x = os.listdir(dir_name)
    # check if the tensors for each date have already been built
    if not (s for s in x if y_date in s):
        print(f'making {y_date}')
    df4 = make_labeled_tensors(x_date, y_date, z_date)

    x = os.listdir(dir_name)
    # combine all the tensor files that have been built
    combined_tensor_df = pd.DataFrame([])
    for i in x:
        if i.startswith('tensor_df_set_'):
            j = dir_name + i
            print(f'reading {j}')
            df1 = pd.read_csv(j, compression='gzip')
            print(df1.shape)
            combined_tensor_df = combined_tensor_df.append(df1)
    print(f'final shape: {combined_tensor_df.shape}')

    combined_tensor_df_name = dir_name + 'combined_tensor_df.csv'
    combined_tensor_df.to_csv(combined_tensor_df_name, compression='gzip', index=False)

if __name__ == "__main__":
    print ('running tensor_time.py')
    a = '2021-03-31'
    b = '2021-04-01'
    c = '2021-04-05'
    a = '2021-04-06'

    make_training_tensors(b, c, a)

    print(f'{Path(__file__).resolve()} completed')

