import pandas as pd
from api_calls import get_option_df, get_stock_df
import os
import sys
import datetime as dt
import argparse

def run_nope(**kwargs):

    nope_dir_name = '../nope_dataframes/'
    if not os.path.exists(nope_dir_name):
        os.mkdir(nope_dir_name)

    pd.set_option('display.max_rows', 800)

    # find the latest stock dataframe
    # later, replace this with something that just makes nope_dfs for every outstanding stock data frame
    stock_dir_name = '../stock_dataframes/'
    stock_df_list = [i for i in os.listdir(stock_dir_name) if (i.endswith('.csv') and not i.endswith('_synth.csv'))]
    print (stock_df_list)
    if 'date_to_run' in kwargs.keys():
        latest_i = kwargs['date_to_run'] + '.csv'
        #input(f'latest_i is: {latest_i}')
    else:
        latest = dt.datetime.now() - dt.timedelta(days=5)
        for i in stock_df_list:
            if i.endswith('.csv'):
                j = i.replace('.csv', '')
                try:
                    csv_time = dt.datetime.strptime(j, "%Y-%m-%d_%H.%M")
                except:
                    csv_time = 0
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
    option_df_list = [i for i in os.listdir(option_dir) if i.endswith('.csv')]
    print (option_dir)
    print (option_df_list)
    if len(option_df_list) == 0:
        print (f'option dataframes not present for {option_dir}')
        return 0

    nope_df = pd.DataFrame()

    count = 0
    for symbol in stock_df['symbol'].unique():
        count +=1
        print (f'{count} -- {symbol}')

        # just find the latest dated option df.
        # later, replace this with something that gets close to the stock timestamp
        try:
            volume = stock_df[stock_df['symbol'] == symbol]['vl'].item()
            adv_21 = stock_df[stock_df['symbol'] == symbol]['adv_21'].item()
            option_df_name = [(option_dir + i) for i in option_df_list if i.startswith((symbol + '_'))][0]
            option_df = pd.read_csv(option_df_name, compression='gzip')

            # find weighted delta
            greeks = ['idelta',
                      'igamma',
                      'itheta',
                      'ivega']
            for g in greeks:
                o_name = f'weighted_{g}'
                option_df[o_name] = option_df['vl'] * option_df[g]

            net_delta = option_df['weighted_idelta'].sum()

            nope_metric = net_delta / volume
            nope_21 = net_delta / adv_21

            option_df['weighted_igamma'] = option_df['vl'] * option_df['igamma']
            net_gamma = option_df['weighted_igamma'].sum()

            noge = net_gamma / volume
            noge_21 = net_gamma / adv_21

            a = {'date': fname_root,
                 'symbol': symbol,
                 'nope_metric': nope_metric,
                 'nope_adv_21': nope_21,
                 'net_idelta': net_delta,
                 'net_igamma': net_gamma,
                 'noge': noge,
                 'noge_21': noge_21}

            temp_df = pd.DataFrame([a])
            for g in greeks:
                t_name = f'mw_{g}'
                o_name = f'weighted_{g}'
                temp_df[t_name] = option_df[o_name].mean()
            nope_df = nope_df.append(temp_df, ignore_index=True)
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

    return 1

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-d', '--date_to_run',
                        help='Enter -d 2021-02-24_09.45',
                        required=False)
    args = vars(parser.parse_args())

    if args['date_to_run'] != None:
        print(args)
        run_nope(date_to_run=date_to_run)
    else:
        run_nope()



