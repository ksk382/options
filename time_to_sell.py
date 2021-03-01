from api_calls import get_holdings, sell_stock, get_stock_df
import datetime as dt
from pytz import timezone
import pandas as pd
import json

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
    for i in holdings['holding']:
        symbol = i['instrument']['sym']
        qty = i['qty']
        purchase_price = i['purchaseprice']
        # find latest bid price, but make sure it isn't zero or something way off
        company_df, e = get_stock_df(symbol)
        if check_fresh(company_df):
            last_bid = company_df.loc[0, 'bid']
            print (f'{symbol}, qty: {qty}, purchase price: {purchase_price}, last_bid: {last_bid}')
            input(f'press enter to sell at last bid')
            r = sell_stock(symbol, qty, last_bid)
            print (r)

if __name__ == "__main__":
    sell_all()