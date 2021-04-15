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

def api_quote(symbol, headers):

    canonical_querystring = 'token=' + access_key
    canonical_uri = f'/v1/stock/{symbol}/quote'
    endpoint = "https://" + host + canonical_uri
    request_url = endpoint + '?' + canonical_querystring
    r = requests.get(request_url, headers=headers)
    d = r.json()
    df = pd.DataFrame([d])
    return df

def query_quote():

    headers = get_auth_headers()
    ticker_list = load_ticker_list()

    now = dt.datetime.now()
    now_str = dt.datetime.strftime(now, "%Y-%m-%d_%H.%M")
    print(now_str)

    quote_dir_name = '../quote_dataframes/'
    if not os.path.exists(quote_dir_name):
        os.mkdir(quote_dir_name)
    fname = now_str + '.csv'
    quote_save_name = quote_dir_name + fname
    if os.path.isfile(quote_save_name):
        all_quote_df = pd.read_csv(quote_save_name, compression='gzip')
    else:
        all_quote_df = pd.DataFrame()
        all_quote_df['symbol'] = ''

    print('&&&&&----- beginning loop')
    count = 0
    exception_count = 0
    error_list = []
    for symbol in ticker_list:
        count+=1
        print(f'{count} getting {symbol} data')
        try:
            e = api_quote(symbol, headers)
            all_quote_df = all_quote_df.append(e, ignore_index=True)
            # save every 100 tickers
            if count % 100 == 0:
                print(f'{count} writing to {quote_save_name}')
                all_quote_df.to_csv(quote_save_name, compression='gzip', index=False)

        except Exception as e:
            exception_count += 1
            print(symbol, '---', str(e))
            error_list.append([symbol, str(e)])
            if exception_count > 2:
                time.sleep(2)

    all_quote_df.to_csv(quote_save_name, compression='gzip', index=False)
    print (f'&&&&&& loop completed. exception count: {exception_count}')
    print (error_list)
    print (all_quote_df)
    return

if __name__ == '__main__':
    start = time.time()
    query_quote()
    end = time.time()
    x = str(dt.timedelta(seconds=(end - start)))
    print (f'Elapsed time: {x}')
    print(f'{Path(__file__).resolve()} completed')