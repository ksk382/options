from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())
import os
import pandas as pd
import json
from api_calls import get_holdings, get_orders


def post_buy_report():
    rec_path = '../recs/'
    flist = [(rec_path + i) for i in os.listdir(rec_path) if i.endswith('.csv')]
    fname = max(flist, key=os.path.getctime)
    df = pd.read_csv(fname, compression='gzip')
    e = get_holdings()
    print(json.dumps(e, indent = 4, sort_keys=True))

    for i in e['holding']:
        sym = i['instrument']['sym']
        print (sym)
        print (i['purchaseprice'])
        df.loc[df['symbol'] == sym,'purchase_price'] = i['purchaseprice']
        df.loc[df['symbol'] == sym,'cost_basis'] = i['costbasis']
    df.to_csv(fname, compression = 'gzip', index=False)
    df['purchase_price'] = df['purchase_price'].apply(pd.to_numeric)
    df['num_to_buy'] = df['num_to_buy'].apply(pd.to_numeric)
    df['x'] = df['purchase_price'] * df['num_to_buy']
    print (df)
    return df

def post_sell_report():
    e = get_orders()




    return

if __name__ == "__main__":

    post_sell_report()