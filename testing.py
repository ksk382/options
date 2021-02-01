# -*- coding: utf-8 -*-
import requests
from cred_file import *
from io import StringIO
import xml.etree.ElementTree as ET
import pandas as pd
import datetime as dt
import os

ticker_df = pd.read_csv('IWV_holdings.csv')
ticker_list = list(ticker_df['Ticker'].unique())
etf_df = pd.read_csv('etf_ticker_list.csv')
ticker_list = ticker_list + list(etf_df['Ticker'].unique())
print (ticker_list)