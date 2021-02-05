import pandas as pd
from api_calls import get_option_df, get_stock_df
import os
import sys
import datetime as dt


def nope_one_off(ticker, stock_df, option_df, now_str):
    nope_dir_name = '../nope_dataframes/'
    if not os.path.exists(nope_dir_name):
        os.mkdir(nope_dir_name)

    nope_df_name = nope_dir_name + now_str + '_nope.csv'
    print (nope_df_name)
    if os.path.exists(nope_df_name):
        nope_df = pd.read_csv(nope_df_name, compression = 'gzip')
        if len(nope_df[nope_df['ticker'] == ticker].index) != 0:
            print (f'already have {ticker}')
            return
    else:
        nope_df = pd.DataFrame([])

    volume = stock_df[stock_df['symbol'] == ticker]['vl'].item()
    adv_21 = stock_df[stock_df['symbol'] == ticker]['adv_21'].item()

    # find weighted delta
    option_df['weighted_delta'] = option_df['vl'] * option_df['idelta']
    net_delta = option_df['weighted_delta'].sum()

    nope_metric = net_delta / volume
    nope_21 = net_delta / adv_21

    option_df['weighted_gamma'] = option_df['vl'] * option_df['igamma']
    net_gamma = option_df['weighted_gamma'].sum()

    noge = net_gamma / volume
    noge_21 = net_gamma / adv_21

    a = {'date': now_str,
         'ticker': ticker,
         'nope_metric': nope_metric,
         'nope_adv_21': nope_21,
         'net_delta': net_delta,
         'net_gamma': net_gamma,
         'noge': noge,
         'noge_21': noge_21}

    nope_df = nope_df.append(a, ignore_index=True)
    print(f'writing to {nope_df_name}')
    nope_df.to_csv(nope_df_name, compression='gzip', index=False)

    pd.set_option('display.max_rows', 800)

    return

def run_nope(**kwargs):

    nope_dir_name = '../nope_dataframes/'
    if not os.path.exists(nope_dir_name):
        os.mkdir(nope_dir_name)

    pd.set_option('display.max_rows', 800)

    # find the latest stock dataframe
    # later, replace this with something that just makes nope_dfs for every outstanding stock data frame
    stock_dir_name = '../stock_dataframes/'
    stock_df_list = os.listdir(stock_dir_name)
    print (stock_df_list)
    if 'date_to_run' in kwargs.keys():
        latest_i = kwargs['date_to_run'] + '.csv'
    else:
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
        print (latest, latest_i)

    #latest_i = '2021-02-01 21.57.csv'
    fname_root = latest_i.replace('.csv', '')
    print (fname_root)

    stock_df_name = stock_dir_name + latest_i
    print (f'stock_df_name: {stock_df_name}')
    stock_df = pd.read_csv(stock_df_name, compression='gzip')

    print (stock_df['symbol'].unique())
    print (len(stock_df['symbol'].unique()))

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

            # find weighted delta
            option_df['weighted_delta'] = option_df['vl'] * option_df['idelta']
            net_delta = option_df['weighted_delta'].sum()

            nope_metric = net_delta / volume
            nope_21 = net_delta / adv_21

            option_df['weighted_gamma'] = option_df['vl'] * option_df['igamma']
            net_gamma = option_df['weighted_gamma'].sum()

            noge = net_gamma / volume
            noge_21 = net_gamma / adv_21

            a = {'date': fname_root,
                 'ticker': ticker,
                 'nope_metric': nope_metric,
                 'nope_adv_21': nope_21,
                 'net_delta': net_delta,
                 'net_gamma': net_gamma,
                 'noge': noge,
                 'noge_21': noge_21}

            nope_df = nope_df.append(a, ignore_index=True)
        except Exception as e:
            print (str(e))
            continue

    print (nope_df)
    j = [i for i in option_df_list if i.endswith('.csv')]
    k = stock_df['symbol'].unique()
    print (f'total unique stocks:       {len(k)}')
    print (f'total unique option_dfs:   {len(j)}')
    print ('stock name: ', stock_df_name)
    print ('option_dir_name: ', option_dir)


    nope_df_name = nope_dir_name + fname_root + '_nope.csv'
    print (f'writing to {nope_df_name}')
    nope_df.to_csv(nope_df_name, compression = 'gzip', index = False)

    return

if __name__ == '__main__':
    #date_to_run = input("enter date to run:\n")
    #run_nope(date_to_run = '2021-02-03_15.30')
    now_str = '2021-02-04_15.30'
    ticker = 'NVDA'
    stock_dir_name = '../stock_dataframes/'
    stock_df_name = stock_dir_name + now_str + '.csv'
    stock_df = pd.read_csv(stock_df_name, compression = 'gzip')
    option_dir = '../option_dataframes/' + now_str + '/'
    option_df_list = os.listdir(option_dir)
    option_df_name = [(option_dir + i) for i in option_df_list if i.startswith((ticker + '_'))][0]
    option_df = pd.read_csv(option_df_name, compression='gzip')

    print (stock_df)
    nope_one_off(ticker, stock_df, option_df, now_str)





