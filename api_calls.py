# -*- coding: utf-8 -*-
import requests
from cred_file import *
from io import StringIO
import xml.etree.ElementTree as ET
import pandas as pd
import datetime as dt
from cred_file import oauth_hdr, stock_endpoint, option_endpoint



def get_option_df(ticker):
    now = dt.datetime.now()
    year = str(now.year)
    month = str(now.month)
    q = f'&query=xyear-eq%3A{year}' #%20AND%20xmonth-eq%3A{month}'
    target_url = option_endpoint + ticker + q
    r = requests.get(url=target_url, auth=oauth_hdr)
    tree = ET.parse(StringIO(r.text))
    root = tree.getroot()
    data = []
    inner = {}
    for child in root.find('.//quotes'):
        for dild in child:
            inner[dild.tag] = dild.text
        data.append(inner)
        inner = {}
    df = pd.DataFrame(data)
    df = df.apply(pd.to_numeric, errors='ignore')

    return df


def get_stock_df(ticker):
    target_url = stock_endpoint + ticker
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

if __name__ == "__main__":
    pd.set_option('display.max_rows', 500)
    print ('starting')
    df = get_stock_df('AAPL')
    print (df)
