# -*- coding: utf-8 -*-
import requests
from cred_file import *
from io import StringIO
import xml.etree.ElementTree as ET
import pandas as pd
import datetime as dt

def get_stock_quote(ticker):
    target_url = 'https://devapi.invest.ally.com/v1/market/ext/quotes.xml?symbols=' + ticker
    r = requests.get(url=target_url, auth=oauth_hdr)
    tree = ET.parse(StringIO(r.text))
    root = tree.getroot()
    data = []
    inner = {}
    for child in root.find('.//quotes'):
        if child.tag == 'quote':
            for dild in child:
                inner[dild.tag] = dild.text
            data.append(inner)
            inner = {}
    df = pd.DataFrame(data)
    df = df.apply(pd.to_numeric, errors='ignore')
    return df

df = get_stock_quote('AAPL')
pd.set_option('display.max_rows', 500)
print (df)
print (df.columns)
print (df.loc[0])
