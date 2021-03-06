from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())
from api_calls import get_holdings, sell_stock, get_stock_df
import datetime as dt
from pytz import timezone
import pandas as pd
import json
import time

def check_fresh(x):
    x['bid_time'] = pd.to_datetime(x['bid_time'])
    x['datetime'] = pd.to_datetime(x['datetime'])
    eastern = timezone('US/Eastern')
    bid_time = eastern.localize(x.loc[0, 'bid_time'])
    response_time = x.loc[0, 'datetime']
    if bid_time > (response_time - dt.timedelta(minutes=3)):
        print (f'bid_time: {bid_time} response_time: {response_time} -- (fresh)')
        return True
    else:
        print(f'bid_time: {bid_time} response_time: {response_time} -- (stale)')
        return False

def sell_all():

    holdings = get_holdings()
    #print (holdings)
    print(json.dumps(holdings, indent=4, sort_keys=True))
    count = 1
    while (len(holdings['holding']) > 0) & (count < 5):
        print (f'Sell all holdings, round: {count}')
        for i in holdings['holding']:
            symbol = i['instrument']['sym']
            qty = i['qty']
            purchase_price = i['purchaseprice']
            # find latest bid price, but make sure it isn't zero or something way off
            try:
                company_df, e = get_stock_df(symbol)
                if check_fresh(company_df):
                    last_bid = company_df.loc[0, 'bid']
                    print(f'\n\n{symbol}, qty: {qty}, purchase price: {purchase_price}, last_bid: {last_bid}\n')
                    # input(f'press enter to sell at last bid')
                    r = sell_stock(symbol, qty, last_bid)
                    print(r)
            except Exception as e:
                print (f'failed to sell {symbol}')
                print (str(e))
        count += 1
        holdings = get_holdings()
        h = len(holdings['holding'])
        print (f'length of holdings: {h}')
        if h > 0 & count > 2:
            time.sleep(30)
    print ('holdings remaining:')
    print (holdings['holding'])
    return

if __name__ == "__main__":
    time.sleep(1)
    sell_all()