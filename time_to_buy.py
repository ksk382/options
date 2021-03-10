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
    rec_df['proj_val'] = rec_df['num_to_buy'] * rec_df['close_price']
    total_val = rec_df['proj_val'].sum()

    while total_val < balance:
        amnt_per_stock += 1
        rec_df['num_to_buy'] = round(amnt_per_stock / rec_df['close_price'], 0)
        rec_df['proj_val'] = rec_df['num_to_buy'] * rec_df['close_price']
        total_val = rec_df['proj_val'].sum()
    amnt_per_stock -= 1
    rec_df['num_to_buy'] = round(amnt_per_stock / rec_df['close_price'], 0)
    rec_df['proj_val'] = rec_df['num_to_buy'] * rec_df['close_price']
    rec_df = rec_df.sort_values(by='num_to_buy', ascending=False)
    rec_df['num_to_buy'] = rec_df['num_to_buy'].values.astype(int)

    return rec_df

def main(**kwargs):
    pd.set_option('display.max_rows', 800)
    pd.set_option('display.min_rows', 200)
    # initialize option save folder
    decision_dir_name = '../decision_dataframes/'
    if not os.path.exists(decision_dir_name):
        os.mkdir(decision_dir_name)

    if 'fname' in kwargs.keys():
        fname = kwargs['fname']
    else:
        print ('update fname')
        return

    out_name = decision_dir_name + fname

    try:
        rec_df = pd.read_csv(f'../nope_dataframes/{fname}', compression='gzip')
    except:
        print (f'no file {fname}')
        return

    rec_df = rec_df[rec_df['buy']==1]
    print (rec_df)
    #rec_df['exec_trade'] = ''

    rec_df = calc_num_buys(rec_df)
    print (rec_df)
    rec_df['last'] = ''
    rec_df['bought'] = ''

    for index, row in rec_df.iterrows():
        symbol = row['symbol']
        price = row['close_price']
        h = row['hurdle_price']
        num_to_buy = row['num_to_buy']

        # make api call to determine current ask price
        try:
            company_df, rate_remaining = get_stock_df(symbol)
        except Exception as exc:
            print (str(exc))
            print (row)
            print ('rate_remaining:', rate_remaining)
            continue

        last_ask = company_df.loc[0,'ask']
        last_ask = float(last_ask)
        rec_df.at[index, 'last'] = last_ask
        hurdle_buffer = h * .99
        # check if current ask price is within a tolerance range of the modeled closing price
        if last_ask < hurdle_buffer:
            print ('would buy')
            buy_amnt = num_to_buy * last_ask
            num_to_buy = str(num_to_buy)
            # increasing limit price for better execution
            limit_price = str(round(hurdle_buffer,1))
            print(f'{symbol}, rec_price: {price}, hurdle_price: {h}, limit_price: {limit_price}' 
                  f'qty: {num_to_buy}, buy_amnt: {buy_amnt}')
            #decision = input('press enter to buy')
            #if decision != 'n':
            buy_report = buy_stock(symbol, num_to_buy, limit_price)
            print (buy_report)
            rec_df.at[index, 'bought'] = buy_amnt
            #else:
            #    print ('not bought')
            #    rec_df.at[index, 'bought'] = 0
            rec_df.to_csv(out_name, compression='gzip', index=False)
        else:
            rec_df.at[index, 'bought'] = 0
            print ('no')
            rec_df.to_csv(out_name, compression='gzip', index=False)

    print (rec_df)
    print (rec_df['bought'].sum())
    print (len(rec_df[rec_df['bought']>0].index))
    rec_df.to_csv(out_name, compression='gzip', index=False)

if __name__ == '__main__':
    today_str = '2021-03-10_14.30'
    h = '0.0098'
    fname = f'recs_{today_str}_hurdle--{h}.csv'
    print (fname)
    input('enter')
    main(fname = fname)