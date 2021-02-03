# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import os
import time
import numpy as np
import seaborn as sns


def merge_stock_with_nope(before, after):

       before_nope_file = f'../nope_dataframes/{before}_nope.csv'
       nope_df = pd.read_csv(before_nope_file, compression = 'gzip')
       nope_df['symbol'] = nope_df['ticker']
       before_stock_file = f'../stock_dataframes/{before}.csv'
       df = pd.read_csv(before_stock_file, compression = 'gzip')

       after_stock_file = f'../stock_dataframes/{after}.csv'
       after_stock_df = pd.read_csv(after_stock_file, compression = 'gzip')
       df['before'] = df['last']
       before_lasts = df[['symbol', 'before']]
       after_stock_df = pd.merge(after_stock_df, before_lasts, on=['symbol'])
       after_stock_df['change_from_before'] = (after_stock_df['last'] - after_stock_df['before']) / after_stock_df['before']
       df = pd.merge(after_stock_df, nope_df, on=['symbol'])
       return df

pd.set_option('display.max_rows', 800)
before = '2021-02-02_16.19'
after = '2021-02-03_09.30'
df2 = merge_stock_with_nope(before,after)

before = '2021-02-01_21.57'
after = '2021-02-02_16.19'
df1 = merge_stock_with_nope(before,after)

df3 = pd.DataFrame([])

for i in ['op','hi','lo','cl']:
       j = i + '_pctchg_1d'
       df3[j] = (df2[i] - df1[i]) / df1[i]

print (df3)

cols = ['adp_100',
       'adp_200',
       'adp_50',
       'adv_21',
       'adv_30',
       'adv_90',
       'ask',
       'ask_time',
       'asksz',
       'basis',
       'beta',
       'bid',
       'bid_time',
       'bidsz',
       'bidtick',
       'chg',
       'chg_sign',
       'chg_t',
       'cl',
       'contract_size',
       'cusip',
       'date_x',
       'datetime',
       'days_to_expiration',
       'div',
       'divexdate',
       'divfreq',
       'divpaydt',
       'dollar_value',
       'eps',
       'exch',
       'exch_desc',
       'hi',
       'iad',
       'idelta',
       'igamma',
       'imp_volatility',
       'incr_vl',
       'irho',
       'issue_desc',
       'itheta',
       'ivega',
       'last',
       'lo',
       'name',
       'op_delivery',
       'op_flag',
       'op_style',
       'op_subclass',
       'openinterest',
       'opn',
       'opt_val',
       'pchg',
       'pchg_sign',
       'pcls',
       'pe',
       'phi',
       'plo',
       'popn',
       'pr_adp_100',
       'pr_adp_200',
       'pr_adp_50',
       'pr_date',
       'pr_openinterest',
       'prbook',
       'prchg',
       'prem_mult',
       'put_call',
       'pvol',
       'qcond',
       'rootsymbol',
       'secclass',
       'sesn',
       'sho',
       'strikeprice',
       'symbol',
       'tcond',
       'timestamp',
       'tr_num',
       'tradetick',
       'trend',
       'under_cusip',
       'undersymbol',
       'vl',
       'volatility12',
       'vwap',
       'wk52hi',
       'wk52hidate',
       'wk52lo',
       'wk52lodate',
       'xdate',
       'xday',
       'xmonth',
       'xyear',
       'yield',
       'before',
       'change_from_before',
       'date_y',
       'net_delta',
       'net_gamma',
       'noge',
       'noge_21',
       'nope_adv_21',
       'nope_metric',
       'ticker']




