# -*- coding: utf-8 -*-
import requests
from cred_file import *
from io import StringIO
import xml.etree.ElementTree as ET
import pandas as pd
import datetime as dt
import os
import time


s = pd.DataFrame([])
for i in range(0,13):
    time.sleep(.1)
    s = s.append({'call_time':time.time()}, ignore_index= True)

print (s)
y = time.time() - 1
print (y)
q = s[s['call_time']>y]
print (q)
print (len(s))
print (len(q))