# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def check_results():
    pd.set_option('display.max_rows', 800)
    pd.set_option('display.min_rows', 200)

    rec_file = '../nope_dataframes/recs_2021-02-11_15.00.csv'
    today_file = '../stock_dataframes/2021-02-12_09.45_synth.csv'
    a = pd.read_csv(rec_file, compression = 'gzip')
    b = pd.read_csv(today_file, compression= 'gzip')
    x = pd.merge(a, b, on='symbol')
    cols = ['symbol','close_price','hurdle','confidence','buy','opn_s']
    x = x[cols]
    x = x[x['buy']==1]
    x['profit'] = ((x['opn_s'] - x['close_price']) / x['close_price']) * x['buy']
    x = x.sort_values(by='profit', ascending=False)

    print (x)

    r = x['profit'].sum() / x['buy'].sum()
    print (f'num bets: {len(x.index)}')
    print (f'return: {r}')
    #sns.regplot(x['pred'], x['profit'])
    #plt.show()

if __name__ == "__main__":
    check_results()