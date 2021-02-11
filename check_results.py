# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from get_rec import get_rec
from build_tensors import make_rec_tensors
from get_rec import get_rec
import os

def check_results():
    pd.set_option('display.max_rows', 800)
    pd.set_option('display.min_rows', 200)

    rec_file = '../nope_dataframes/recs_2021-02-10_15.00.csv'
    today_file = '../stock_dataframes/2021-02-11_09.45_synth.csv'
    a = pd.read_csv(rec_file, compression = 'gzip')
    b = pd.read_csv(today_file, compression= 'gzip')
    b = b[b['opn']!=0]
    x = pd.merge(a, b, on='symbol')
    cols = ['symbol','cl_s_y','pred','buy','opn']
    x = x[cols]
    pr_date = b['pr_date'].iloc[0]
    h = pr_date + ' close'
    today_date = b['date'].iloc[0]
    i = today_date + ' open'
    cols2 = ['symbol',h,'pred','buy',i]
    x.columns = cols2
    x = x[x['buy']==1]
    x['profit'] = ((x[i] - x[h]) / x[h]) * x['buy']
    x = x.sort_values(by='profit', ascending=False)



    print (x)

    r = x['profit'].sum() / x['buy'].sum()
    print (f'num bets: {len(x.index)}')
    print (f'return: {r}')
    #sns.regplot(x['pred'], x['profit'])
    #plt.show()
