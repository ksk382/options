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

def api_stat(symbol, headers, access_key):

    canonical_querystring = 'token=' + access_key
    canonical_uri = f'/v1/stock/{symbol}/stats'
    endpoint = "https://" + host + canonical_uri
    request_url = endpoint + '?' + canonical_querystring
    r = requests.get(request_url, headers=headers)
    d = r.json()
    df = pd.DataFrame([d])
    return df

def main():

    now = dt.datetime.now()
    now_str = dt.datetime.strftime(now, "%Y-%m-%d_%H.%M")
    print(now_str)

    stock_dir_name = '../stat_dataframes/'
    if not os.path.exists(stock_dir_name):
        os.mkdir(stock_dir_name)
    fname = now_str + '.csv'
    stock_save_name = stock_dir_name + fname
    if os.path.isfile(stock_save_name):
        all_stock_df = pd.read_csv(stock_save_name, compression='gzip')
    else:
        all_stock_df = pd.DataFrame()
        all_stock_df['symbol'] = ''

    access_key = os.environ.get('IEX_PUBLIC_KEY')
    headers = get_auth_headers()
    print ('headers:\n')
    print (headers)

    error_list = []
    ticker_list = load_ticker_list()
    print('&&&&&----- beginning loop')

    count = 0
    exception_count = 0
    for symbol in ticker_list:
        count += 1
        print(f'{count} getting {symbol} data')
        #try:
        if symbol in all_stock_df['symbol'].unique():
            print(f'Already have {symbol}')
        stock_df = api_stat(symbol, headers, access_key)
        stock_df['symbol'] = symbol
        all_stock_df = all_stock_df.append(stock_df, ignore_index=True)

        # save every 100 tickers
        if count % 100 == 0:
            print(f'{count} writing to {stock_save_name}')
            all_stock_df.to_csv(stock_save_name, compression='gzip', index=False)

        '''except Exception as e:
            exception_count += 1
            print(symbol,'---', str(e))
            error_list.append([symbol, str(e)])
            if exception_count > 2:
                time.sleep(2)'''

    all_stock_df.to_csv(stock_save_name, compression='gzip', index=False)
    print (f'&&&&&& loop completed. exception count: {exception_count}')
    print (error_list)

if __name__ == '__main__':
    main()