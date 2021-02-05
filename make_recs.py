import pandas as pd
from get_rec import get_rec
from build_tensors import make_rec_tensors
from get_rec import get_rec



def make_recs(now_str):
    pd.set_option('display.max_rows', 800)
    pd.set_option('display.min_rows', 200)

    today_stock_file = f'../stock_dataframes/{now_str}.csv'
    df2 = pd.read_csv(today_stock_file, compression='gzip')

    pr_date = df2['pr_date'].head(1).item() + '_15.30'
    yesterday_stock_file = f'../stock_dataframes/{pr_date}.csv'
    df1 = pd.read_csv(yesterday_stock_file, compression='gzip')

    today_nope = f'../nope_dataframes/{now_str}_nope.csv'
    nope_df = pd.read_csv(today_nope, compression='gzip')
    nope_df['symbol'] = nope_df['ticker']

    sp_500_df = pd.read_csv('sp500_ticker_list.csv', compression='gzip')

    df = make_rec_tensors(df1, df2, nope_df, sp_500_df)
    print(df)
    rec_df = get_rec(df)
    print(rec_df)
    rec_df.to_csv(f'../nope_dataframes/recs_{now_str}.csv', compression='gzip', index=False)
    return rec_df

def check_results():
    pd.set_option('display.max_rows', 800)
    pd.set_option('display.min_rows', 200)

    rec_file = '../nope_dataframes/recs_2021-02-04_15.30.csv'
    today_file = '../stock_dataframes/2021-02-05_09.30.csv'
    a = pd.read_csv(rec_file, compression = 'gzip')
    b = pd.read_csv(today_file, compression= 'gzip')
    x = pd.merge(a, b, on='symbol')
    cols = ['symbol','last_y','pred','buy','opn','last']
    x = x[cols]
    x = x[x['buy']==1]
    x['result1'] = (x['last_y'] - x['opn']) * x['buy']
    print (x)
    r = x['result1'].sum() / x['buy'].sum()
    print (r)

if __name__ == "__main__":
    now_str = '2021-02-04_15.30'
    #df = make_recs(now_str)
    check_results()

