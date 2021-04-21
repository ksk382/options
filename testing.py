import pandas as pd
import os
import datetime as dt
from api_calls import get_stock_df, get_balance, sell_stock, buy_stock, acct_num, get_holdings
import json
import pandas as pd

def latest_file(dir_name, today_str):
    flist = [(dir_name + i) for i in os.listdir(dir_name) if
             (i.endswith('.csv') and i.startswith(today_str) and
              not i.endswith('_16.30.csv') and not i.endswith('synth.csv'))]
    #fname = max(flist, key=os.path.getctime)
    fname = sorted(flist)[-1]
    return fname

f = latest_file('../quote_dataframes/', '2021-04-09')
print (f)