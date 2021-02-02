# -*- coding: utf-8 -*-
import requests
from cred_file import *
from io import StringIO
import xml.etree.ElementTree as ET
import pandas as pd
import datetime as dt
import os
import time

df = pd.read_csv('../stock_dataframes/2021-02-01_21.21.csv', compression = 'gzip')
print (df)

a = len(df['symbol'].unique())
print (a)