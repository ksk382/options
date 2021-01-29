import pandas as pd
from option_api import get_option_df
import datetime as dt
import os

ticker_list = pd.read_csv('ticker_list.csv')
now = dt.datetime.now()
print (now)

today = str(now)[:10]
dir_name = '../option_dataframes/'+today + '/'
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
err_output_file = '../logs/' + now_str + '_error_list.txt'
count = 0
for ticker in ticker_list['Ticker'].unique():
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
    else:
        print (f'{count} - {ticker} already done in last hour')


for i in error_list:
    print (i)
print (len(error_list))
