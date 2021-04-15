from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())
import pandas as pd
import datetime as dt
import os
import numpy as np
import argparse
import time

pd.set_option('display.max_rows', 800)


def latest_file(dir_name, today_str):
    flist = [(dir_name + i) for i in os.listdir(dir_name) if
             (i.endswith('.csv') and i.startswith(today_str) and
              not i.endswith('_16.30.csv') and not i.endswith('synth.csv'))]
    print (flist)
    fname = max(flist, key=os.path.getctime)
    return fname

def merge_df_files(today_str):

    # run this once for each day
    # creates combined dataframe that then gets fed into data munging

    first_dir = '../stock_dataframes/'
    second_dir = '../stat_dataframes/'
    third_dir = '../nope_dataframes/'
    out_dir = '../combined_dataframes/'

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    df1_name = latest_file(first_dir, today_str)
    df2_name = latest_file(second_dir, today_str)
    df3_name = latest_file(third_dir, today_str)
    print ('df names:')
    print (df1_name, df2_name, df3_name)
    df1 = pd.read_csv(df1_name, compression = 'gzip')
    df2 = pd.read_csv(df2_name, compression = 'gzip')
    df3 = pd.read_csv(df3_name, compression = 'gzip')

    df4 = pd.merge(df1, df2, on=['symbol'])
    df4 = pd.merge(df4, df3, on=['symbol'])

    df4['df_date'] = today_str

    sp_500_df = pd.read_csv('sp500_ticker_list.csv', compression='gzip')
    etf_df = pd.read_csv('etf_ticker_list.csv', compression='gzip')
    qqq_df = pd.read_csv('qqq_ticker_list.csv', compression='gzip')
    df4['sp'] = df4['symbol'].isin(sp_500_df['Ticker']) * 1
    df4['etf'] = df4['symbol'].isin(etf_df['Ticker']) * 1
    df4['qqq'] = df4['symbol'].isin(qqq_df['symbol']) * 1
    # consider adding SPY performance of that day as a data point

    out_name = f'{out_dir}{today_str}.csv'
    df4.to_csv(out_name, compression='gzip', index=False)
    print (df4.iloc[0])
    return

if __name__ == "__main__":

    start = time.time()
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-d', '--date_to_run',
                        help='Enter -d 2021-02-24',
                        required=False)
    args = vars(parser.parse_args())

    if args['date_to_run'] != None:
        today_str = args['date_to_run']
    else:
        now = dt.datetime.now()
        today_str = dt.datetime.strftime(now, "%Y-%m-%d")
    print (f'running merge_df_files: {today_str}')
    merge_df_files(today_str)
    end = time.time()
    x = str(dt.timedelta(seconds=(end - start)))
    print(f'Elapsed time: {x}')
    print(f'{Path(__file__).resolve()} completed')