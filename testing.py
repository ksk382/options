# -*- coding: utf-8 -*-
import requests
from cred_file import *
from io import StringIO
import xml.etree.ElementTree as ET
import pandas as pd
import datetime as dt
import os
import time
import numpy as np

df = pd.read_csv('../nope_dataframes/2021-02-02_17.30_nope.csv', compression = 'gzip')
pd.set_option('display.max_rows', 200)
pd.set_option('display.min_rows', None)

df = df.round(5)
df = df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]
print (df)

df = df.sort_values(by='Nope_adv_21', ascending = False)
print (df)
