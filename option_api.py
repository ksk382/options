# -*- coding: utf-8 -*-
import requests
from cred_file import *
from io import StringIO
import xml.etree.ElementTree as ET
import pandas as pd
import datetime as dt


def get_option_df(ticker):

    now = dt.datetime.now()
    year = str(now.year)
    month = str(now.month)
    q = f'&query=xyear-eq%3A{year}' #%20AND%20xmonth-eq%3A{month}'
    target_url = 'https://devapi.invest.ally.com/v1/market/options/search.xml?symbol=' + ticker + q
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

if __name__ == "__main__":
    pd.set_option('display.max_rows', 500)
    print ('starting')
    df = get_option_df('AAPL')
    print (df)