import pandas as pd
from gather import load_ticker_list
import os
import datetime as dt

'''

Need to get clean data that shows day -1 ohlcv, day 0 ohlcv, and day +1 o

'''
def clean_up(**kwargs):

    pd.set_option('display.min_rows', 50)
    pd.set_option('display.max_rows', 200)

    ticker_list = load_ticker_list()
    o_dir = '../ohlcv/'
    s_dir = '../stock_dataframes/'
    if 'date_to_run' in kwargs.keys():
        now_str = kwargs['date_to_run'] + '.csv'
        stock_df_name = [i for i in os.listdir(s_dir) if i.startswith(now_str)]
        today_str = now_str
    else:
        list_of_files = [(s_dir + i) for i in os.listdir(s_dir) if i.endswith('.csv')]
        stock_df_name = max(list_of_files, key=os.path.getctime)
        today_str = os.listdir(o_dir)[0][-14:-4]

    #today = dt.datetime.now()
    #today_str = today.strftime("%Y-%m-%d")

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

    df = pd.read_csv(stock_df_name, compression = 'gzip')
    d = df['date'].iloc[0]
    x = odf_all[odf_all['date_s']==d]
    out_df = pd.merge(df, x, on='symbol')

    j = stock_df_name.replace('.csv', '')
    out_name = s_dir + j + '_synth.csv'
    print(out_name)
    out_df.to_csv(out_name, compression = 'gzip', index = False)

    print (out_df.columns)
    print (out_df.tail())

if __name__=='__main__':
    clean_up()


