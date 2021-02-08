import pandas as pd
from gather import load_ticker_list
import os
import datetime as dt

'''

Need to get clean data that shows day -1 ohlcv, day 0 ohlcv, and day +1 o

'''
def clean_up():

    pd.set_option('display.min_rows', 50)
    pd.set_option('display.max_rows', 200)

    ticker_list = load_ticker_list()
    o_dir = '../ohlcv/'
    s_dir = '../stock_dataframes/'
    s_list = [i for i in os.listdir(s_dir) if i.endswith('15.30.csv')]
    today = dt.datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    print (s_list)

    odf_all = pd.DataFrame([])
    for ticker in ticker_list:
        o_name = o_dir + ticker + '_' + today_str + '.csv'
        try:
            odf = pd.read_csv(o_name, compression = 'gzip')
            odf['ticker'] = ticker
            #print (odf.tail())
            odf_all = odf_all.append(odf, ignore_index=True)
        except:
            continue


    print (odf_all.tail())
    odf_all.columns = ['opn_s','hi_s','lo_s','cl_s','adj_cl_s', 'vl_s','date_s','symbol']
    print ('loaded ohlcv')
    print (odf_all.tail())

    for i in s_list:
        fname = s_dir + i
        d = i[:10]
        df = pd.read_csv(fname, compression = 'gzip')
        j = i.replace('.csv', '')
        out_name = s_dir + j + '_synth.csv'
        print (out_name)
        x = odf_all[odf_all['date_s']==d]
        out_df = pd.merge(df, x, on='symbol')
        out_df.to_csv(out_name, compression = 'gzip', index = False)

    print (out_df.columns)
    print (out_df.tail())

if __name__=='__main__'()
    clean_up()


