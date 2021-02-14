import pandas as pd
import datetime as dt
from api_calls import get_stock_df, get_balance, sell_stock, buy_stock, acct_num
import numpy as np
import os

def calc_num_buys(rec_df):
    # determine how much of each stock to buy
    balance = get_balance()
    num_stocks = len(rec_df.index)
    amnt_per_stock = balance / num_stocks
    rec_df['num_to_buy'] = round(amnt_per_stock / rec_df['close_price'], 0)
    rec_df['value'] = rec_df['num_to_buy'] * rec_df['close_price']
    total_val = rec_df['value'].sum()

    while total_val < balance:
        amnt_per_stock += 1
        rec_df['num_to_buy'] = round(amnt_per_stock / rec_df['close_price'], 0)
        rec_df['value'] = rec_df['num_to_buy'] * rec_df['close_price']
        total_val = rec_df['value'].sum()
    amnt_per_stock -= 1
    rec_df['num_to_buy'] = round(amnt_per_stock / rec_df['close_price'], 0)
    rec_df['value'] = rec_df['num_to_buy'] * rec_df['close_price']
    rec_df = rec_df.sort_values(by='num_to_buy', ascending=False)
    total_val = rec_df['value'].sum()

    return rec_df

def main(**kwargs):
    pd.set_option('display.max_rows', 800)
    pd.set_option('display.min_rows', 200)
    # initialize option save folder
    decision_dir_name = '../decision_dataframes/'
    if not os.path.exists(decision_dir_name):
        os.mkdir(decision_dir_name)

    if 'date_to_run' in kwargs.keys():
        now_str = kwargs['date_to_run']
    else:
        now = dt.datetime.now()
        now_str = dt.datetime.strftime(now, "%Y-%m-%d_") +'15.00'
        print(now_str)
    now_str = '2021-02-12_15.00'

    out_name = decision_dir_name + now_str + '.csv'

    rec_df = pd.read_csv(f'../nope_dataframes/recs_{now_str}.csv', compression='gzip')
    rec_df = rec_df[rec_df['buy']==1]
    print (rec_df)
    #rec_df['exec_trade'] = ''

    rec_df = calc_num_buys(rec_df)
    print (rec_df)

    for index, row in rec_df.iterrows():
        symbol = row['symbol']
        price = row['close_price']
        h = row['hurdle_price']
        num_to_buy = row['num_to_buy']
        print (symbol, price, h, num_to_buy)
        # make api call to determine current ask price
        company_df, e = get_stock_df(company)
        last_price = company_df.loc[0,'last']
        # check if current ask price is within a tolerance range of the modeled closing price

        if last_price < (price * 1.005):
            buy_report = buy_stock(symbol, num_to_buy, last_price)
            print (symbol)
            print (buy_report)


    rec_df.to_csv(out_name, compression='gzip', index=False)

if __name__ == '__main__':
    main()