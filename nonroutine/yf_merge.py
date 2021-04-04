import datetime as dt
import os
import pandas as pd
import argparse

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
    open_df = open_df.drop_duplicates()
    print (open_df)
    open_df.to_csv(fname, compression='gzip', index=False)


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
        print(stock_df_name)

    #today = dt.datetime.now()
    #today_str = today.strftime("%Y-%m-%d")
    odf_all = pd.DataFrame([])
    o_file_list = [(o_dir + i) for i in os.listdir(o_dir) if (i.endswith('csv') and not i.endswith('_openprices.csv'))]
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

    print (odf_all.tail())

    odf_all.columns = ['opn_s','hi_s','lo_s','cl_s','adj_cl_s', 'vl_s','date_s','symbol']
    print ('loaded ohlcv')

    df = pd.read_csv(stock_df_name, compression = 'gzip')
    d = df['date'].iloc[0]
    x = odf_all[odf_all['date_s']==d]
    print ('x tail: \n')
    print (x.tail())
    out_df = pd.merge(df, x, on='symbol')
    out_df = out_df.drop_duplicates()

    out_name = stock_df_name.replace('.csv', '_synth.csv')
    print(out_name)
    out_df.to_csv(out_name, compression = 'gzip', index = False)

    print (out_df.columns)
    print (out_df.tail())
    print (f'full shape: {out_df.shape}')


def interval_merge():

    # merges ohlcv_hourly data with stock dataframes
    pd.set_option('display.min_rows', 50)
    pd.set_option('display.max_rows', 200)

    o_dir = '../ohlcv_hourly/'
    s_dir = '../stock_dataframes/'

    s_name = '2021-03-04_14.30.csv'

    o_name = o_dir + 'AAPL.csv'
    odf = pd.read_csv(o_name, compression='gzip')
    odf['Datetime'] = pd.to_datetime(odf['Datetime'])
    odf['Date'] = odf['Datetime'].dt.date
    print (odf)

    df = odf.iloc[6::7, :]
    print (df)

    for k in ['Adj Close', 'Volume']:
        m = k + '_end'
        odf[m] = odf[k][6::7]
        for i in range(0,6):
            j = 5 - i
            odf.at[j::7, m] = odf[m].shift(-(i+1))

    odf['cl_mvm'] = (odf['Adj Close_end'] - odf['Adj Close']) / odf['Adj Close']
    odf['vlm_mvm'] = (odf['Volume_end'] - odf['Volume']) / odf['Volume']

    print (odf)

    return


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-d', '--date_to_run',
                        help='Enter -d 2021-02-24_09.45',
                        required=False)
    args = vars(parser.parse_args())

    if args['date_to_run'] != None:
        print(args)
        yf_merge(date_to_run=args['date_to_run'])
    else:
        print(args)
        yf_merge()