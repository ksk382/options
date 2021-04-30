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
now = dt.datetime.now()
today_str = dt.datetime.strftime(now, "%Y-%m-%d")

rec_path = '../recs/'
start_string = rec_path + f'recs_{today_str}'
flist = [(rec_path + i) for i in os.listdir(rec_path) if i.endswith('.csv') and i.startswith(start_string)]

try:
    latest_file = max(flist, key=os.path.getctime)
    print (latest_file)
except:
    print ('no rec file found for today...exiting')
    sys.exit()
