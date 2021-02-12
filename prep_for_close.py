from nope import run_nope
from clean_up import clean_up
from ohlcv_retrieve import yf_ohlcv, clear_ohlcv
import datetime as dt
import os

if __name__=='__main__':
    #now = dt.datetime.now()
    #today_str = dt.datetime.strftime(now, "%Y-%m-%d")

    s_dir = '../stock_dataframes/'
    list_of_files = [(s_dir + i) for i in os.listdir(s_dir) if (i.endswith('.csv') and not i.endswith('_synth.csv'))]
    stock_df_name = max(list_of_files, key=os.path.getctime)
    time_str = stock_df_name.replace(s_dir,'').replace('.csv','')

    x = run_nope(date_to_run=time_str)
    if x == 1:
        clear_ohlcv()
        yf_ohlcv()
        clean_up()
        print (f'\n\n\n\n&&&&&----- Nope, ohlcv, and clean_up complete')
    else:
        print ('nope did not complete')