# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import requests
from cred_file import *
from io import StringIO
import pandas as pd
import datetime as dt
import os
import time
import numpy as np
import seaborn as sns
import xml.etree.ElementTree as ET
import pandas as pd
import datetime as dt
from cred_file import oauth_hdr, stock_endpoint, option_endpoint
import json
import pprint


def get_stock_df(ticker):
    target_url = stock_endpoint + ticker
    r = requests.get(url=target_url, auth=oauth_hdr)
    d = json.loads(r.text)
    #print(json.dumps(d, indent = 4, sort_keys=True))
    d = d['response']['quotes']['quote']
    df = pd.DataFrame([d])
    e = r.headers['X-RateLimit-Remaining']
    return df, e

def get_option_df(ticker):
    now = dt.datetime.now()
    year = str(now.year)
    #month = str(now.month)
    q = f'&query=xyear-eq%3A{year}' #%20AND%20xmonth-eq%3A{month}'
    target_url = option_endpoint + ticker + q
    r = requests.get(url=target_url, auth=oauth_hdr)
    d = json.loads(r.text)
    #print(json.dumps(d, indent = 4, sort_keys=True))
    d = d['response']['quotes']['quote']
    df = pd.DataFrame(d)
    e = r.headers['X-RateLimit-Remaining']
    return df, e


df, rate_remaining = get_option_df('AAPL')
print (df)
print (rate_remaining)