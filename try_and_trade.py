from tensor_time import munge
import os
import pandas as pd
import datetime as dt
from api_auth import get_auth_headers
from query_quote import api_quote
from api_calls import get_stock_df, get_balance, sell_stock, buy_stock, acct_num, get_holdings



def calc_num_buys(rec_df):
    # determine how much of each stock to buy
    balance = get_balance()
    print ('balance: ', balance)
    num_stocks = len(rec_df.index)
    print ('num stocks to buy:', num_stocks)
    amnt_per_stock = balance / num_stocks
    print ('amnt per stock:', amnt_per_stock)
    rec_df['num_to_buy'] = round((amnt_per_stock / rec_df['last_ask']), 0)
    rec_df['proj_val'] = rec_df['num_to_buy'] * rec_df['last_ask']
    total_val = rec_df['proj_val'].sum()

    while total_val < balance:
        amnt_per_stock += 1
        rec_df['num_to_buy'] = round(amnt_per_stock / rec_df['last_ask'], 0)
        rec_df['proj_val'] = rec_df['num_to_buy'] * rec_df['last_ask']
        total_val = rec_df['proj_val'].sum()
    amnt_per_stock -= 1
    rec_df['num_to_buy'] = round(amnt_per_stock / rec_df['last_ask'], 0)
    rec_df['proj_val'] = rec_df['num_to_buy'] * rec_df['last_ask']
    rec_df = rec_df.sort_values(by='num_to_buy', ascending=False)
    rec_df['num_to_buy'] = rec_df['num_to_buy'].values.astype(int)

    return rec_df

if __name__ == "__main__":

    rec_path = '../recs/'
    flist = [(rec_path + i) for i in os.listdir(rec_path) if i.endswith('.csv')]
    latest_file = max(flist, key=os.path.getctime)

    z = pd.read_csv(latest_file, compression='gzip')

    buy_bucket = pd.DataFrame()
    z['last_ask'] = ''
    z['buy_at_price'] = 0
    for index, row in z.iterrows():
        symbol = row['symbol']

        # make api call to determine current ask price
        #try:
        company_df, rate_remaining = get_stock_df(symbol)

        last_ask = company_df.loc[0, 'ask']
        last_ask = float(last_ask)
        z.at[index, 'last_ask'] = last_ask

        if last_ask < row['ba_hurdle']:
            z.at[index, 'buy_at_price'] = 1
        '''except Exception as exc:
            print(str(exc))
            # print(row)
            print('rate_remaining:', rate_remaining)
            last_ask = 10000000
            continue'''

    z['last_ask'] = pd.to_numeric(z['last_ask'])
    print(z[['symbol', 'hurdle_price', 'ba_spread',
             'ba_hurdle', 'last_ask', 'buy', 'buy_at_price']])
    will_buy = z[z['buy_at_price'] == 1]
    buy_amnts = calc_num_buys(will_buy)
    print(buy_amnts)

    hurdle = buy_amnts.iloc[0]['hurdle']
    now = dt.datetime.now()
    today_str = dt.datetime.strftime(now, "%Y-%m-%d")

    out_name = rec_path + f'rec_{today_str}_hurdle--{hurdle}.csv'
    z.to_csv(out_name, compression='gzip', index=False)
    out_name = rec_path + f'rec_{today_str}_hurdle--{hurdle}_buy_amnts.csv'
    buy_amnts.to_csv(out_name, compression='gzip', index=False)

    input('***hit enter to send orders***')

    for index, row in buy_amnts.iterrows():
        limit_price = min(row['last_ask'], round(row['ba_hurdle'], 2))
        num_to_buy = str(row['num_to_buy'])
        print(row['symbol'], num_to_buy, limit_price)
        # input('enter')
        buy_report = buy_stock(row['symbol'], num_to_buy, limit_price)
        print(buy_report)

