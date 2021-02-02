# -*- coding: utf-8 -*-
import requests
from cred_file import *
from io import StringIO
import xml.etree.ElementTree as ET
import pandas as pd
import datetime as dt
import os

df = pd.read_csv('2021-02-01 21.57_nope.csv', compression = 'gzip')
