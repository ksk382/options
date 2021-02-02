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
    all_stock_df = pd.DataFrame()
    now_str = dt.datetime.strftime(now, "%Y-%m-%d_%H.%M")
    fname = now_str + '.csv'
    stock_save_name = stock_dir_name + fname

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
    start_time = time.time()
    for ticker in ticker_list:
        try:
            stock_df = get_stock_df(ticker)
            count += 1
            print (f'{count} retrieved {ticker} stock')
            option_df = get_option_df(ticker)
            count += 1
            print (f'{count} retrieved {ticker} option chain')

            all_stock_df = all_stock_df.append(stock_df, ignore_index=True)
            # save every 100 calls
            if count % 100 == 0:
                print (f'{count} writing to {stock_save_name}')
                all_stock_df.to_csv(stock_save_name, compression='gzip', index=False)

            option_save_name = option_dir_name + ticker + '_.csv'
            print (f'{count} writing {option_save_name}')
            option_df.to_csv(option_save_name, compression='gzip', index=False)

        except Exception as e:
            print (ticker, str(e))
            error_list.append([ticker, str(e)])
            with open(err_output_file, 'a') as f:
                f.write("%s\n" % [ticker, str(e)])

        time.sleep(1)

        ''' this rate limiter does not work
        elapsed_time = (time.time() - start_time) * 60
        rate = (count / elapsed_time)
        while rate >= 60:
            elapsed_time = (time.time() - start_time) * 60
            rate = (count / elapsed_time)
            print (f'sleeping...count: {count} elapsed_time: {round(elapsed_time,2)} rate: {round(rate,2)}')
            time.sleep(1)'''

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
