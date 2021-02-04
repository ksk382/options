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


df = pd.read_csv('sp500_ticker_list.csv')
print (df)

before_stock_file = f'../nope_dataframes/2021-02-03_15.30_nope.csv'
df2 = pd.read_csv(before_stock_file, compression = 'gzip')
print (df2.columns)
