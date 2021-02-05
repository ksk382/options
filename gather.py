import pandas as pd
from api_calls import get_option_df, get_stock_df
import datetime as dt
import os
import time
from nope import nope_one_off


def gather_stock_and_option_data(**kwargs):
    print ('\n\n\n\n&&&&&----- gathering stock and option data\n\n')

    # gather the tickers to use
    ticker_list = load_ticker_list()

    if 'kow_str' in kwargs.keys():
        now_str = kwargs['kow_str']
    else:
        now = dt.datetime.now()
        now_str = dt.datetime.strftime(now, "%Y-%m-%d_%H.%M")
        print (now_str)

    print ('&&&&&----- beginning loop')

    error_list = run_loop(ticker_list, now_str)

    retry_list = []
    for i in error_list:
        retry_list.append(i[0])
    error_list_2 = run_loop(retry_list, now_str)

    print ('error_list: ')
    for i in error_list_2:
        print (i)
    print (f'{len(error_list)} errors')

    print ('\n\n\n\n&&&&&----- done gathering stock and option data\n\n')

    return

def load_ticker_list():
    ticker_df = pd.read_csv('IWV_holdings.csv')
    ticker_list = list(ticker_df['Ticker'].unique())
    etf_df = pd.read_csv('etf_ticker_list.csv')
    ticker_list = ticker_list + list(etf_df['Ticker'].unique())
    print('ticker list:')
    print(ticker_list)
    return ticker_list

def gather_stock_data(**kwargs):
    print('\n\n\n\n&&&&&----- gathering stock and option data\n\n')

    # gather the tickers to use
    ticker_list = load_ticker_list()

    if 'kow_str' in kwargs.keys():
        now_str = kwargs['kow_str']
    else:
        now = dt.datetime.now()
        now_str = dt.datetime.strftime(now, "%Y-%m-%d_%H.%M")
        print(now_str)

    print('&&&&&----- beginning loop')

    error_list = run_stock_loop(ticker_list, now_str)

    retry_list = []
    for i in error_list:
        retry_list.append(i[0])
    error_list_2 = run_stock_loop(retry_list, now_str)

    print('error_list: ')
    for i in error_list_2:
        print(i)
    print(f'{len(error_list)} errors')

    print('\n\n\n\n&&&&&----- done gathering stock data\n\n')

    return

def run_stock_loop(ticker_list, now_str):
    stock_dir_name = '../stock_dataframes/'
    fname = now_str + '.csv'
    stock_save_name = stock_dir_name + fname
    if os.path.isfile(stock_save_name):
        all_stock_df = pd.read_csv(stock_save_name, compression='gzip')
    else:
        all_stock_df = pd.DataFrame()
        all_stock_df['symbol'] = ''

    # initialize option save folder
    option_dir_name = '../option_dataframes/' + now_str + '/'
    if not os.path.exists('../option_dataframes/'):
        os.mkdir('../option_dataframes/')
    if not os.path.exists(option_dir_name):
        os.mkdir(option_dir_name)

    error_list = []
    count = 0
    exception_count = 0
    for ticker in ticker_list:
        count += 1
        print(f'{count} getting {ticker} data')
        if ticker in all_stock_df['symbol'].unique():
            print(f'Already have {ticker}')
        else:
            try:
                stock_df, stock_rate_remaining = get_stock_df(ticker)
                print(f'{count} of {len(ticker_list)} retrieved {ticker} stock. Rate remaining: {stock_rate_remaining}')
                all_stock_df = all_stock_df.append(stock_df, ignore_index=True)

                # save every 100 tickers
                if count % 100 == 0:
                    print(f'{count} writing to {stock_save_name}')
                    all_stock_df.to_csv(stock_save_name, compression='gzip', index=False)

                # rate limiting
                try:
                    rate_remaining = int(stock_rate_remaining)
                except:
                    rate_remaining = 20

                if rate_remaining < 10:
                    sleep_time = (15 - rate_remaining)
                    print(f'{count} of {len(ticker_list)} rate_remaining: {rate_remaining} ---- sleeping {sleep_time} seconds')
                    time.sleep(sleep_time)
                exception_count = 0

            except Exception as e:
                exception_count += 1
                print(ticker, str(e))
                error_list.append([ticker, str(e)])
                if exception_count > 2:
                    time.sleep(2)

    print(f'{count} writing to {stock_save_name}')
    all_stock_df.to_csv(stock_save_name, compression='gzip', index=False)


def run_loop(ticker_list, now_str):

    stock_dir_name = '../stock_dataframes/'
    fname = now_str + '.csv'
    stock_save_name = stock_dir_name + fname
    if os.path.isfile(stock_save_name):
        all_stock_df = pd.read_csv(stock_save_name, compression='gzip')
    else:
        all_stock_df = pd.DataFrame()
        all_stock_df['symbol'] = ''

    # initialize option save folder
    option_dir_name = '../option_dataframes/' + now_str + '/'
    if not os.path.exists('../option_dataframes/'):
        os.mkdir('../option_dataframes/')
    if not os.path.exists(option_dir_name):
        os.mkdir(option_dir_name)

    error_list = []
    count = 0
    exception_count = 0
    for ticker in ticker_list:
        count += 1
        print (f'{count} getting {ticker} data')
        if ticker in all_stock_df['symbol'].unique():
            print (f'Already have {ticker}')
        else:
            try:
                stock_df, stock_rate_remaining = get_stock_df(ticker)
                print (f'{count} of {len(ticker_list)} retrieved {ticker} stock. Rate remaining: {stock_rate_remaining}')

                option_df, option_rate_remaining = get_option_df(ticker)
                print (f'{count} of {len(ticker_list)} retrieved {ticker} option chain. Rate remaining: {option_rate_remaining}')

                all_stock_df = all_stock_df.append(stock_df, ignore_index=True)

                # save every 100 tickers
                if count % 100 == 0:
                    print (f'{count} writing to {stock_save_name}')
                    all_stock_df.to_csv(stock_save_name, compression='gzip', index=False)

                option_save_name = option_dir_name + ticker + '_.csv'
                print (f'{count} of {len(ticker_list)} writing to {option_save_name}')
                option_df.to_csv(option_save_name, compression='gzip', index=False)

                # nope_one_off(ticker, stock_df, option_df)
                # also put a tensor_one_off here

                # rate limiting
                try:
                    rate_remaining = int(min(stock_rate_remaining, option_rate_remaining))
                except:
                    rate_remaining = 20

                if rate_remaining < 10:
                    sleep_time = (15 - rate_remaining)
                    print (f'{count} of {len(ticker_list)} rate_remaining: {rate_remaining} ---- sleeping {sleep_time} seconds')
                    time.sleep(sleep_time)

                exception_count = 0

            except Exception as e:
                exception_count += 1
                print (ticker, str(e))
                error_list.append([ticker, str(e)])
                if exception_count > 2:
                    time.sleep(2)

    print (f'{count} writing to {stock_save_name}')
    all_stock_df.to_csv(stock_save_name, compression='gzip', index=False)

    return error_list


if __name__ == "__main__":
    #now_str = '2021-02-03_15.30'
    #gather_stock_and_option_data(kow_str = now_str)
    #gather_stock_and_option_data()
    gather_stock_data()
