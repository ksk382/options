import pandas as pd
from api_calls import get_option_df, get_stock_df
import datetime as dt
import os
import time
from nope import run_nope


def gather_stock_and_option_data():
    print ('\n\n\n\n&&&&&----- gathering stock and option data\n\n')

    # gather the tickers to use
    ticker_df = pd.read_csv('IWV_holdings.csv')
    ticker_list = list(ticker_df['Ticker'].unique())
    etf_df = pd.read_csv('etf_ticker_list.csv')
    ticker_list = ticker_list + list(etf_df['Ticker'].unique())
    print ('ticker list:')
    print (ticker_list)

    # initialize stock dataframe
    stock_dir_name = '../stock_dataframes/'
    now = dt.datetime.now()
    print (now)
    if not os.path.exists(stock_dir_name):
        os.mkdir(stock_dir_name)
    now_str = dt.datetime.strftime(now, "%Y-%m-%d_%H.%M")
    # or you can manually pick up an unfinished pull
    # now_str = '2021-02-02_16.19'
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

    # initialize error logging
    err_output_file = '../logs/' + now_str + '_stock_error_list.txt'
    error_list = []

    count = 0
    # set up a rate limiter
    s = pd.DataFrame([])
    exception_count = 0
    for ticker in ticker_list:
        count += 1
        print (f'{count} getting {ticker} data')
        if ticker in all_stock_df['symbol'].unique():
            print (f'Already have {ticker}')
        else:
            try:
                stock_df, stock_rate_remaining = get_stock_df(ticker)
                s = s.append({'call_time': time.time()}, ignore_index=True)
                print (f'{count} of {len(ticker_list)} retrieved {ticker} stock')

                option_df, option_rate_remaining = get_option_df(ticker)
                s = s.append({'call_time': time.time()}, ignore_index=True)
                print (f'{count} of {len(ticker_list)} retrieved {ticker} option chain')

                all_stock_df = all_stock_df.append(stock_df, ignore_index=True)

                # save every 100 tickers
                if count % 100 == 0:
                    print (f'{count} writing to {stock_save_name}')
                    all_stock_df.to_csv(stock_save_name, compression='gzip', index=False)

                option_save_name = option_dir_name + ticker + '_.csv'
                print (f'{count} of {len(ticker_list)} writing to {option_save_name}')
                option_df.to_csv(option_save_name, compression='gzip', index=False)

                # rate limiting
                rate_remaining = min(stock_rate_remaining, option_rate_remaining)
                if rate_remaining < 10:
                    sleep_time = -(10 - rate_remaining)
                    print (f'{count} of {len(ticker_list)} rate_remaining: {rate_remaining} ---- sleeping {sleep_time} seconds')
                    time.sleep(sleep_time)

                '''
                # alternate rate limiting code
                y = time.time() - 60
                q = s[s['call_time'] > y]
                breaker = 0
                while len(q) > 58 or breaker > 10:
                    sleep_time = (len(q) - 58)
                    print (f'number of calls in last minute: {len(q)} ---- sleeping {sleep_time} seconds')
                    time.sleep(sleep_time)
                    y = time.time()
                    q = s[s['call_time'] > y]
                    breaker +=1
                exception_count = 0
                '''

            except Exception as e:
                exception_count += 1
                print (ticker, str(e))
                error_list.append([ticker, str(e)])
                with open(err_output_file, 'a') as f:
                    f.write("%s\n" % [ticker, str(e)])
                if exception_count > 2:
                    time.sleep(2)

    print (f'{count} writing to {stock_save_name}')
    all_stock_df.to_csv(stock_save_name, compression='gzip', index=False)

    print ('error_list: ')
    for i in error_list:
        print (i)
    print (f'{len(error_list)} errors')

    print ('\n\n\n\n&&&&&----- done gathering stock and option data\n\n')

    return

if __name__ == "__main__":

    gather_stock_and_option_data()
    run_nope()
