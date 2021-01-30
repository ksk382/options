import pandas as pd
from api_calls import get_option_df, get_stock_df
import datetime as dt
import os
import time


def gather_option_data():
    print ('-----gathering option data')
    #ticker_list = pd.read_csv('ticker_list.csv')
    ticker_df = pd.read_csv('IWV_holdings.csv')
    ticker_list = ticker_df['Ticker'].unique()
    now = dt.datetime.now()
    print (now)

    today = str(now)[:10]
    dir_name = '../option_dataframes/'+today + '/'
    if not os.path.exists('../option_dataframes/'):
        os.mkdir('../option_dataframes/')
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    existing_files = os.listdir(dir_name)
    existing_files = [i for i in existing_files if i.endswith('.csv')]

    done_tickers = []
    now = dt.datetime.now()
    for i in existing_files:
        d = i.replace('.csv','')
        d = d[-len('2021-01-29 14.13'):]
        done_ticker = i.replace(d,'').replace('_','').replace('.csv','')
        prev_call_time = dt.datetime.strptime(d, "%Y-%m-%d %H.%M")
        hour_ago = now - dt.timedelta(hours=1)
        if prev_call_time > hour_ago:
            done_tickers.append(done_ticker)

    print ('Already done: ')
    print (done_tickers)

    error_list = []
    now_str = dt.datetime.strftime(now, "%Y-%m-%d %H.%M")
    err_output_file = '../logs/' + now_str + '_option_error_list.txt'
    count = 0
    for ticker in ticker_list:
        count +=1
        if ticker not in done_tickers:
            now = dt.datetime.now()
            try:
                df = get_option_df(ticker)
                fname = ticker + '_' + dt.datetime.strftime(now, "%Y-%m-%d %H.%M") + '.csv'
                filename = dir_name + fname
                print (f'{count} writing {filename}')
                df.to_csv(filename, compression='gzip', index=False)
            except Exception as e:
                print (ticker, str(e))
                error_list.append([ticker, str(e)])
                with open(err_output_file, 'a') as f:
                    f.write("%s\n" % [ticker, str(e)])
            # throttle API calls to 60 per minute
            time.sleep(1)
        else:
            print (f'{count} - {ticker} already done in last hour')

    for i in error_list:
        print (i)
    print (len(error_list))
    print ('-----done gathering option data')

def gather_stock_data():
    print ('-----gathering stock data')
    #ticker_list_df = pd.read_csv('sp500_ticker_list.csv')
    ticker_df = pd.read_csv('IWV_holdings.csv')
    ticker_list = ticker_df['Ticker'].unique()
    print (ticker_list)
    now = dt.datetime.now()
    print (now)

    today = str(now)[:10]
    dir_name = '../stock_dataframes/' + today + '/'
    if not os.path.exists('../stock_dataframes/'):
        os.mkdir('../stock_dataframes/')
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    existing_files = os.listdir(dir_name)
    existing_files = [i for i in existing_files if i.endswith('.csv')]

    done_tickers = []
    now = dt.datetime.now()
    for i in existing_files:
        d = i.replace('.csv', '')
        d = d[-len('2021-01-29 14.13'):]
        done_ticker = i.replace(d, '').replace('_', '').replace('.csv', '')
        prev_call_time = dt.datetime.strptime(d, "%Y-%m-%d %H.%M")
        hour_ago = now - dt.timedelta(hours=1)
        if prev_call_time > hour_ago:
            done_tickers.append(done_ticker)

    error_list = []
    now_str = dt.datetime.strftime(now, "%Y-%m-%d %H.%M")
    err_output_file = '../logs/' + now_str + '_stock_error_list.txt'
    count = 0
    for ticker in ticker_list:
        count += 1
        if ticker not in done_tickers:
            now = dt.datetime.now()
            try:
                df = get_stock_df(ticker)
                fname = ticker + '_' + dt.datetime.strftime(now, "%Y-%m-%d %H.%M") + '.csv'
                filename = dir_name + fname
                print (f'{count} writing {filename}')
                df.to_csv(filename, compression='gzip', index=False)
            except Exception as e:
                print (ticker, str(e))
                error_list.append([ticker, str(e)])
                with open(err_output_file, 'a') as f:
                    f.write("%s\n" % [ticker, str(e)])
            # throttle API calls to 60 per minute
            time.sleep(1)
        else:
            print (f'{count} - {ticker} already done in last hour')

    print ('-----done gathering stock data')

def gather_etf_data():
    print ('-----gathering etf data')


    print ('-----done gathering etf data')

if __name__ == "__main__":
    gather_option_data()
    gather_stock_data()
    #gather_etf_data()