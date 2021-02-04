# -*- coding: utf-8 -*-
import requests
from cred_file import *
import pandas as pd
import datetime as dt
from cred_file import oauth_hdr, stock_endpoint, option_endpoint


def get_stock_df(ticker):
    target_url = stock_endpoint + ticker
    r = requests.get(url=target_url, auth=oauth_hdr)
    #print(json.dumps(d, indent = 4, sort_keys=True))
    d = r.json()['response']['quotes']['quote']
    df = pd.DataFrame([d])
    try:
        e = int(r.headers['X-RateLimit-Remaining'])
    except:
        e = 1
    return df, e

def get_option_df(ticker):
    now = dt.datetime.now()
    year = str(now.year)
    #month = str(now.month)
    q = f'&query=xyear-eq%3A{year}' #%20AND%20xmonth-eq%3A{month}'
    target_url = option_endpoint + ticker + q
    r = requests.get(url=target_url, auth=oauth_hdr)
    #print(json.dumps(d, indent = 4, sort_keys=True))
    d = r.json()['response']['quotes']['quote']
    df = pd.DataFrame(d)
    try:
        e = int(r.headers['X-RateLimit-Remaining'])
    except:
        e = 1
    return df, e

if __name__ == "__main__":
    pd.set_option('display.max_rows', 500)
    print ('starting')
    df = get_stock_df('AAPL')
    print (df)
