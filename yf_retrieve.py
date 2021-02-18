import datetime as dt
import sys
import os
import pandas as pd
import yfinance as yf
from pathlib import Path
from gather import load_ticker_list


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

    '''
    count = 0
    for ticker in ticker_list:
        count +=1
        f_name = f'{save_path}{ticker}_{today_str}.csv'
        if os.path.isfile(f_name):
            print (f'{count} - {ticker} -- exists')
        else:
            print (f'{count} out of {len(ticker_list)} - {ticker}')
            try:
                y = yf.download(ticker, start=earlier_str, end=end_str,
                                group_by="ticker")
                print(f'{count} - {ticker} -- complete')
            except Exception as e:
                print (str(e))
                continue
            x = pd.DataFrame(y)
            x['Date'] = x.index
            x.to_csv(f_name, compression='gzip', index=False)
            if count % 50 == 0:
                root_directory = Path(save_path)
                size = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file()) / 1000000
                print (f'size: {size} MB')
                if size > 500:
                    sys.exit(0)'''
    return


def yf_merge(**kwargs):
    #merges ohlcv data with stock dataframes
    pd.set_option('display.min_rows', 50)
    pd.set_option('display.max_rows', 200)

    o_dir = '../ohlcv/'
    s_dir = '../stock_dataframes/'
    if 'date_to_run' in kwargs.keys():
        now_str = str(kwargs['date_to_run']) + '.csv'
        stock_df_name = [(s_dir + i) for i in os.listdir(s_dir) if (i.startswith(now_str) and not i.endswith('_synth.csv'))][0]
        print (stock_df_name)
    else:
        list_of_files = [(s_dir + i) for i in os.listdir(s_dir) if (i.endswith('.csv') and not i.endswith('_synth.csv'))]
        stock_df_name = max(list_of_files, key=os.path.getctime)

    #today = dt.datetime.now()
    #today_str = today.strftime("%Y-%m-%d")
    odf_all = pd.DataFrame([])
    o_file_list = [(o_dir + i) for i in os.listdir(o_dir) if i.endswith('csv')]
    for o_name in o_file_list:
        #o_name = o_dir + ticker + '_' + odf_str + '.csv'
        try:
            odf = pd.read_csv(o_name, compression = 'gzip')
            ticker = o_name.replace(o_dir, '').replace('.csv', '')
            odf['ticker'] = ticker
            odf_all = odf_all.append(odf, ignore_index=True)
        except Exception as e:
            print (str(e))
            continue

    odf_all.columns = ['opn_s','hi_s','lo_s','cl_s','adj_cl_s', 'vl_s','date_s','symbol']
    print ('loaded ohlcv')

    df = pd.read_csv(stock_df_name, compression = 'gzip')
    d = df['date'].iloc[0]
    x = odf_all[odf_all['date_s']==d]
    print ('x tail: \n')
    print (x.tail())
    out_df = pd.merge(df, x, on='symbol')

    out_name = stock_df_name.replace('.csv', '_synth.csv')
    print(out_name)
    out_df.to_csv(out_name, compression = 'gzip', index = False)

    print (out_df.columns)
    print (out_df.tail())
    print (f'full shape: {out_df.shape}')

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

def yf_retrieve_multi_thread():
    import concurrent.futures
    import urllib.request

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
            print(f'removing {j}')
            os.remove(j)

    # Retrieve a single page and report the URL and contents
    def yf_pull(ticker):
        try:
            y = yf.download(ticker, start=earlier_str, end=end_str,
                            group_by="ticker")
        except Exception as e:
            print (ticker, str(e))
            y = []
        x = pd.DataFrame(y)
        x['Date'] = x.index
        f_name = f'{save_path}{ticker}_{today_str}.csv'
        x.to_csv(f_name, compression='gzip', index=False)
        return y

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for ticker in ticker_list[:20]:
            futures.append(executor.submit(yf_pull, ticker=ticker))
        for future in concurrent.futures.as_completed(futures):
            print(future.result())

def make_today_frame():
    today = dt.datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    fname = f'../ohlcv/{today_str}_openprices.csv'

    o_name = '../ohlcv/'
    x = [i for i in os.listdir(o_name) if i.endswith('.csv')]
    open_df = pd.DataFrame([])
    for i in x:
        ticker = i.replace('.csv', '')
        j = o_name + i
        df = pd.read_csv(j, compression = 'gzip')
        df = df.loc[df['Date'] == today_str]
        df['symbol'] = ticker
        open_df = open_df.append(df)
    print (open_df)
    open_df.to_csv(fname, compression='gzip', index=False)


if __name__ == "__main__":
    #yf_retrieve_multi_thread()
    #yf_ohlcv()
    yf_merge(date_to_run='2021-02-18_09.45')
    #make_today_frame()