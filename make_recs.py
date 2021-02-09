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


def make_recs(now_str):
    pd.set_option('display.max_rows', 800)
    pd.set_option('display.min_rows', 200)

    today_stock_file = f'../stock_dataframes/{now_str}_synth.csv'
    df2 = pd.read_csv(today_stock_file, compression='gzip')

    pr_date = df2['pr_date'].head(1).item()
    stock_df_list = [i for i in os.listdir('../stock_dataframes/') if (i.endswith('_synth.csv') and pr_date in i)]

    yesterday_stock_file = f'../stock_dataframes/{pr_date}_synth.csv'
    df1 = pd.read_csv(yesterday_stock_file, compression='gzip')

    today_nope = f'../nope_dataframes/{now_str}_nope.csv'
    nope_df = pd.read_csv(today_nope, compression='gzip')
    nope_df['symbol'] = nope_df['ticker']

    sp_500_df = pd.read_csv('sp500_ticker_list.csv', compression='gzip')
    etf_df = pd.read_csv('etf_ticker_list.csv', compression='gzip')

    df = make_rec_tensors(df1, df2, nope_df, sp_500_df, etf_df)
    print(df)
    rec_df = get_rec(df)
    rec_df = rec_df.round(3)
    y = rec_df[rec_df['buy'] == 1]
    print (y)
    print (len(y.index))
    print (y['symbol'].unique())
    rec_df.to_csv(f'../nope_dataframes/recs_{now_str}.csv', compression='gzip', index=False)
    return rec_df

def check_results():
    pd.set_option('display.max_rows', 800)
    pd.set_option('display.min_rows', 200)

    rec_file = '../nope_dataframes/recs_2021-02-08_15.30.csv'
    today_file = '../stock_dataframes/2021-02-09_09.30_synth.csv'
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


if __name__ == "__main__":
    now_str = '2021-02-09_15.00'
    df = make_recs(now_str)
    #check_results()

