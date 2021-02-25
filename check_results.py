# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import datetime as dt

def check_results():
    pd.set_option('display.max_rows', 800)
    pd.set_option('display.min_rows', 200)

    today = dt.datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    yest = today - dt.timedelta(days = 1)
    yest_str = yest.strftime("%Y-%m-%d")
    rec_file = f'../nope_dataframes/recs_{yest_str}_14.30.csv'
    n_dir = '../nope_dataframes/'
    list_of_files = [(n_dir + i) for i in os.listdir(n_dir) if (i.startswith(f'recs_{yest_str}'))]
    for j in list_of_files:
        rec_file = j
        #rec_file = f'../nope_dataframes/recs_2021-02-19_14.30.csv'
        today_file = f'../ohlcv/{today_str}_openprices.csv'
        print (rec_file)
        print (today_file)

        a = pd.read_csv(rec_file, compression = 'gzip')
        b = pd.read_csv(today_file, compression= 'gzip')
        x = pd.merge(a, b, on='symbol')
        cols = ['symbol','close_price','hurdle','confidence','buy','Open']
        x = x[cols]
        x = x[x['buy']==1]
        x['profit'] = ((x['Open'] - x['close_price']) / x['close_price']) * x['buy']
        x['profit'] = round(x['profit'],3)
        x = x.sort_values(by='profit', ascending=False)

        print (x)

        r = x['profit'].sum() / x['buy'].sum()
        print (f'num bets: {len(x.index)}')
        print (f'return: {r}')
        #sns.regplot(x['pred'], x['profit'])
        #plt.show()

if __name__ == "__main__":
    check_results()