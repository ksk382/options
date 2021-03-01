import datetime as dt
import sys
import os
import pandas as pd
import yfinance as yf
from pathlib import Path
from gather import load_ticker_list
import argparse


pd.set_option('display.max_rows', 2000)
pd.set_option('display.min_rows', 100)

def clear_ohlcv():
    save_path = '../ohlcv/'
    if not os.path.exists(save_path):
        print('path doesnt exist')
        return

    x = [(save_path + i) for i in os.listdir(save_path) if i.endswith('.csv')]
    for i in x:
        os.remove(i)
    return

def yf_ohlcv():

    ticker_list = load_ticker_list()
    today = dt.datetime.now()
    # 253 trading days in a year
    days_back = 20
    DD = dt.timedelta(days=days_back)
    earlier = today - DD
    earlier_str = earlier.strftime("%Y-%m-%d")
    today_str = today.strftime("%Y-%m-%d")
    end_str = today + dt.timedelta(days=1)

    save_path = '../ohlcv/'
    if os.path.exists(save_path):
        print('path exists')
    else:
        os.mkdir(save_path)

    contents = os.listdir(save_path)
    s = today_str + '.csv'
    for i in contents:
        if not i.endswith(s):
            j = save_path + i
            print (f'removing {j}')
            os.remove(j)

    data = yf.download(ticker_list, start=earlier_str, end=end_str,
                                group_by="ticker")
    print (data)
    data = data.T

    for ticker in ticker_list:
        df = data.loc[(ticker,),].T
        df['Date'] = df.index
        df.to_csv('../ohlcv/' + ticker + '.csv', compression='gzip', index=False)

    return


def yf_gather_info():
    # grab fundamental info
    save_path = '../yf_info/'
    if os.path.exists(save_path):
        print('path exists')
    else:
        os.mkdir(save_path)
    existing_files = os.listdir(save_path)

    ticker_list = load_ticker_list()
    today = dt.datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    count = 0
    for ticker in ticker_list:
        for i in [j for j in existing_files if (j.startswith((ticker+'_')) and not j.endswith(f'{today_str}.csv')) ]:
            m = save_path + i
            try:
                print (f'deleting {m}')
                os.remove(m)
            except:
                print (f'{m} somehow already gone')
                pass
        count += 1
        f_name = f'{save_path}{ticker}_{today_str}.csv'
        if os.path.isfile(f_name):
            print(f'{count} - {ticker} -- exists')
        else:
            print(f'{count} out of {len(ticker_list)} - {ticker}')
            try:
                y = yf.Ticker(ticker)
                z = y.info
                x = pd.DataFrame([z])
                x.to_csv(f_name, compression='gzip', index=False)

            except Exception as e:
                print(str(e))
                continue

            if count % 50 == 0:
                root_directory = Path(save_path)
                size = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file()) / 1000000
                print(f'size: {size} MB')
                if size > 500:
                    sys.exit(0)
    return

def yf_ohlcv_hourly():

    ticker_list = load_ticker_list()
    today = dt.datetime.now()
    # 253 trading days in a year
    days_back = 60
    DD = dt.timedelta(days=days_back)
    earlier = today - DD
    earlier_str = earlier.strftime("%Y-%m-%d")
    end_str = today + dt.timedelta(days=1)

    save_path = '../ohlcv_hourly/'
    if os.path.exists(save_path):
        print('path exists')
    else:
        os.mkdir(save_path)

    data = yf.download(ticker_list, start=earlier_str, end=end_str,
                                group_by="ticker", interval='60m')
    data = data.T

    count = 0
    for ticker in ticker_list:
        count+=1
        df = data.loc[(ticker,),].T
        df['Datetime'] = df.index
        fname = '../ohlcv_hourly/' + ticker + '.csv'
        if os.path.exists(fname):
            x = pd.read_csv(fname, compression = 'gzip')
            x['Datetime'] = pd.to_datetime(x['Datetime'])
            x.index = x['Datetime']
            df.update(x)
        df['symbol'] = ticker
        df.to_csv(fname, compression='gzip', index=False)
        if count % 100 == 0:
            print (f'Writing to csv. Count: {count}')

if __name__ == "__main__":
    yf_ohlcv_hourly()
