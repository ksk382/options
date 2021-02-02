import pandas as pd
from api_calls import get_option_df, get_stock_df
import os
import sys
import datetime as dt


def run_nope():
    nope_dir_name = '../nope_dataframes/'
    if not os.path.exists(nope_dir_name):
        os.mkdir(nope_dir_name)

    pd.set_option('display.max_rows', 800)

    # find the latest stock dataframe
    # later, replace this with something that just makes nope_dfs for every outstanding stock data frame
    stock_dir_name = '../stock_dataframes/'
    stock_df_list = os.listdir(stock_dir_name)
    print (stock_df_list)
    latest = dt.datetime.now() - dt.timedelta(days=5)
    for i in stock_df_list:
        if i.endswith('.csv'):
            j = i.replace('.csv', '')
            csv_time = dt.datetime.strptime(j, "%Y-%m-%d %H.%M")
            if csv_time > latest:
                latest = csv_time
                latest_i = i
    print (latest, i)
    fname_root = dt.datetime.strftime(latest, "%Y-%m-%d %H.%M")

    stock_df_name = stock_dir_name + i
    stock_df = pd.read_csv(stock_df_name, compression='gzip')

    print (stock_df['symbol'].unique())

    option_dir = '../option_dataframes/' + latest_i[:10] + '/'
    option_df_list = os.listdir(option_dir)

    nope_df = pd.DataFrame()

    count = 0
    for ticker in stock_df['symbol'].unique():
        count +=1
        print (f'{count} -- {ticker}')
        volume = stock_df[stock_df['symbol'] == ticker]['vl'].item()
        adv_21 = stock_df[stock_df['symbol'] == ticker]['adv_21'].item()
        # just find the latest dated option df.
        # later, replace this with something that gets close to the stock timestamp
        try:
            option_df_name = [(option_dir + i) for i in option_df_list if i.startswith((ticker + '_'))][0]
        except:
            continue
        option_df = pd.read_csv(option_df_name, compression = 'gzip')
        option_df['weighted'] = option_df['vl'] * option_df['idelta']
        nope_metric = option_df['weighted'].sum() / volume
        nope_21 = option_df['weighted'].sum() / adv_21
        a = {'Date': fname_root,
             'Ticker': ticker,
             'Nope': nope_metric,
             'Nope_adv_21': nope_21}
        nope_df = nope_df.append(a, ignore_index=True)

    print (nope_df)

    nope_df_name = nope_dir_name + fname_root + '_nope.csv'
    nope_df.to_csv(nope_df_name, compression = 'gzip', index = False)

if __name__ == '__main__':
    run_nope()





