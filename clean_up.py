import pandas as pd
from gather import load_ticker_list
import os
import datetime as dt

'''

Need to get clean data that shows day -1 ohlcv, day 0 ohlcv, and day +1 o

'''
def clean_up(**kwargs):
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
            ticker = o_name.split('_')[0].replace(o_dir, '')
            odf['ticker'] = ticker
            #print (odf.tail())
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

if __name__=='__main__':
    date_to_run = input("enter date to run:\n")
    clean_up(date_to_run=date_to_run)


