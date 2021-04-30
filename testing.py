import pandas as pd
import os
import datetime as dt
from api_calls import get_stock_df, get_balance, sell_stock, buy_stock, acct_num, get_holdings, get_orders
import pandas as pd
from api_auth import get_auth_headers
from cred_file import access_key, host
import requests
from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())
from api_auth import get_auth_headers
import os
import requests
import pandas as pd
import datetime as dt
import time
from cred_file import access_key, host
import json
from api_calls import get_stock_df
import sys

pd.set_option('display.max_rows', 500)

fname = '../recs/rec_2021-04-29_hurdle--0.00853_buy_amnts.csv'
rec_df = pd.read_csv(fname, compression='gzip')

print (rec_df)
print (rec_df.columns)
print (rec_df['symbol'])

quote_df_name = '../quote_dataframes/2021-04-30_09.50.csv'
quote_df = pd.read_csv(quote_df_name, compression = 'gzip')

quote_df = quote_df[['symbol', 'latestPrice']]
quote_df.columns = ['symbol', 'next_day_price']

print (quote_df)
print (quote_df.columns)


x = pd.merge(rec_df, quote_df, on='symbol')

x = x[['symbol',
          'hurdle',
          'hurdle_price',
          'ba_hurdle',
          'confidence',
          'buy',
          'last_ask',
          'buy_at_price',
          'num_to_buy',
          'proj_val',
          'next_day_price']]

x['delta'] = (x['next_day_price'] - x['last_ask']) / x['last_ask']

print (x)
print (x['delta'].mean())
