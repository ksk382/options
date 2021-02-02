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
            try:
                csv_time = dt.datetime.strptime(j, "%Y-%m-%d_%H.%M")
            except:
                csv_time = dt.datetime.strptime(j, "%Y-%m-%d %H.%M")
            if csv_time > latest:
                latest = csv_time
                latest_i = i
    print (latest, i)
    fname_root = dt.datetime.strftime(latest, "%Y-%m-%d_%H.%M")

    latest_i = '2021-02-02_14.30'
    stock_df_name = stock_dir_name + latest_i
    stock_df = pd.read_csv(stock_df_name, compression='gzip')

    print (stock_df['symbol'].unique())

    option_dir = '../option_dataframes/' + latest_i[:-4] + '/'
    option_df_list = os.listdir(option_dir)
    print (option_dir)
    print (option_df_list)

    nope_df = pd.DataFrame()

    count = 0
    for ticker in stock_df['symbol'].unique():
        count +=1
        print (f'{count} -- {ticker}')

        # just find the latest dated option df.
        # later, replace this with something that gets close to the stock timestamp
        try:
            volume = stock_df[stock_df['symbol'] == ticker]['vl'].item()
            adv_21 = stock_df[stock_df['symbol'] == ticker]['adv_21'].item()
            option_df_name = [(option_dir + i) for i in option_df_list if i.startswith((ticker + '_'))][0]
            option_df = pd.read_csv(option_df_name, compression='gzip')
            option_df['weighted'] = option_df['vl'] * option_df['idelta']
            nope_metric = option_df['weighted'].sum() / volume
            nope_21 = option_df['weighted'].sum() / adv_21
            a = {'Date': fname_root,
                 'Ticker': ticker,
                 'Nope': nope_metric,
                 'Nope_adv_21': nope_21}
            nope_df = nope_df.append(a, ignore_index=True)
        except Exception as e:
            print (str(e))
            continue

    print (nope_df)
    j = [i for i in option_df_list if i.endswith('.csv')]
    k = stock_df['symbol'].unique()
    print (f'total unique stocks:       {len(k)}')
    print (f'total unique option_dfs:   {len(j)}')


    nope_df_name = nope_dir_name + fname_root + '_nope.csv'
    print (f'writing to {nope_df_name}')
    nope_df.to_csv(nope_df_name, compression = 'gzip', index = False)

    return

if __name__ == '__main__':
    run_nope()





