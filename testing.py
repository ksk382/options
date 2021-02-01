# -*- coding: utf-8 -*-
import requests
from cred_file import *
from io import StringIO
import xml.etree.ElementTree as ET
import pandas as pd
import datetime as dt
import os

now = dt.datetime.now() - dt.timedelta(days=1)
print (now)
today = str(now)[:10]
print (today)
dir_name = '../stock_dataframes/' + today + '/'
pd.set_option('display.max_rows', 500)

x = os.listdir(dir_name)
a = pd.DataFrame()
for i in x:
    if i.endswith('.csv'):
        j = dir_name + i
        df = pd.read_csv(j, compression = 'gzip')
        df['Ticker'] = i.split('_')[0]
        print (df)
        print (df.columns)
        print (df.loc[0])
        input('enter')
        a = a.append(df, ignore_index = True)
print (a)
a.to_csv('all.csv', compression = 'gzip', index = False)