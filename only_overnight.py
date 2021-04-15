from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())
from api_auth import get_auth_headers
import os
import requests
import pandas as pd
import datetime as dt
import time
from cred_file import access_key, host

def load_ticker_list():
    ticker_df = pd.read_csv('IWV_holdings.csv').dropna()
    ticker_df = ticker_df[ticker_df['Ticker'] != '-']
    ticker_list = list(ticker_df['Ticker'].unique())
    etf_df = pd.read_csv('etf_ticker_list.csv', compression = 'gzip')
    ticker_list = ticker_list + list(etf_df['Ticker'].unique())
    return ticker_list


def api_ohlcv_chart(symbol, headers):
    canonical_querystring = 'token=' + access_key
    canonical_uri = f'/v1/stock/{symbol}/chart/5d'
    endpoint = "https://" + host + canonical_uri
    request_url = endpoint + '?' + canonical_querystring
    try:
        r = requests.get(request_url, headers=headers)
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        time.sleep(3)
        r = requests.get(request_url, headers=headers)
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        return 0
    d = r.json()
    df = pd.DataFrame(d)
    return df

def pull_ohlcv():
    ticker_list = load_ticker_list()
    headers = get_auth_headers()
    ohlcv_save_name = '../ohlcv/ohlcv.csv'

    if os.path.isfile(ohlcv_save_name):
        all_stock_df = pd.read_csv(ohlcv_save_name, compression='gzip')
    else:
        all_stock_df = pd.DataFrame()
        all_stock_df['symbol'] = ''

    count = 0
    exception_count = 0
    error_list = []
    for symbol in ticker_list:
        count += 1
        print(f'{count} getting {symbol} data')
        try:
            if symbol in all_stock_df['symbol'].unique():
                print(f'Already have {symbol}')
            stock_df = api_ohlcv_chart(symbol, headers)
            if stock_df != 0:
                stock_df['symbol'] = symbol
                all_stock_df = all_stock_df.append(stock_df, ignore_index=True)

            # save every 100 tickers
            if count % 100 == 0:
                print(f'{count} writing to {ohlcv_save_name}')
                all_stock_df.to_csv(ohlcv_save_name, compression='gzip', index=False)

        except Exception as e:
            exception_count += 1
            print(symbol, '---', str(e))
            error_list.append([symbol, str(e)])
            if exception_count > 2:
                time.sleep(2)

    all_stock_df.to_csv(ohlcv_save_name, compression='gzip', index=False)
    print(f'&&&&&& loop completed. exception count: {exception_count}')
    print(error_list)
    return

def api_ohlcv_today(symbol, headers):

    canonical_querystring = 'token=' + access_key
    canonical_uri = f'/v1/stock/{symbol}/ohlc'
    endpoint = "https://" + host + canonical_uri
    request_url = endpoint + '?' + canonical_querystring
    r = requests.get(request_url, headers=headers)
    d = r.json()
    df = pd.DataFrame(d)
    return df

def daily_ohlcv():
    ticker_list = load_ticker_list()
    headers = get_auth_headers()
    ohlcv_save_name = '../ohlcv/ohlcv.csv'

    if os.path.isfile(ohlcv_save_name):
        all_stock_df = pd.read_csv(ohlcv_save_name, compression='gzip')
    else:
        all_stock_df = pd.DataFrame()

    count = 0
    exception_count = 0
    error_list = []
    empty_dfs = []
    for symbol in ticker_list:
        count += 1
        #try:
        stock_df = api_ohlcv_today(symbol, headers)
        if not stock_df.empty:
            epochtime = stock_df['open']['time']
            stock_df['datetime'] = pd.to_datetime(stock_df['open']['time'], unit='ms')
            stock_df['datetime'] = stock_df['datetime'].dt.tz_localize('utc').dt.tz_convert('US/Eastern').dt.round('1s')
            stock_df['date'] = stock_df['datetime'].dt.date
            y = time.strftime('%Y-%m-%d', time.gmtime(epochtime / 1000.))
            stock_df = stock_df.T['price']
            stock_df['date'] = y
            all_stock_df = all_stock_df.append(stock_df, ignore_index=True)
            print(f'{count} saved {symbol} data')
        else:
            print(f'{count}-------no data for {symbol}-------')
            empty_dfs.append(symbol)
        # save every 100 tickers
        if count % 100 == 0:
            print(f'{count} writing to {ohlcv_save_name}')
            all_stock_df.to_csv(ohlcv_save_name, compression='gzip', index=False)

        '''
        except Exception as e:
            exception_count += 1
            print(symbol, '---', str(e))
            error_list.append([symbol, str(e)])
            if exception_count > 2:
                time.sleep(2)'''

    all_stock_df = all_stock_df.drop_duplicates(subset=['symbol', 'date'], keep='first')
    all_stock_df.to_csv(ohlcv_save_name, compression='gzip', index=False)
    print(f'&&&&&& loop completed. exception count: {exception_count}')
    print('error_list: ')
    print(error_list)
    print('empty dataframes:')
    print(empty_dfs)
    print('length of empty dataframes: ', len(empty_dfs))
    return

if __name__ == '__main__':

    # functions that should not run during market hours
    start = time.time()
    daily_ohlcv()
    end = time.time()
    x = str(dt.timedelta(seconds=(end - start)))
    print(f'Elapsed time: {x}')
    print(f'{Path(__file__).resolve()} completed')