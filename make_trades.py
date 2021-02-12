import pandas as pd
import datetime as dt
from api_calls import get_stock_df

def main(**kwargs):
    pd.set_option('display.max_rows', 800)
    pd.set_option('display.min_rows', 200)

    if 'date_to_run' in kwargs.keys():
        now_str = kwargs['date_to_run']
    else:
        now = dt.datetime.now()
        now_str = dt.datetime.strftime(now, "%Y-%m-%d_") +'15.00'
        print(now_str)

    rec_df = pd.read_csv(f'../nope_dataframes/recs_{now_str}.csv', compression='gzip')
    rec_df = rec_df[rec_df['buy']==1]
    print (rec_df)
    rec_df['hurdle_price'] = rec_df['close_price'] + rec_df['close_price'] * rec_df['hurdle']
    rec_df['exec_trade'] = ''
    for index, row in rec_df.iterrows():
        company = row['symbol']
        price = row['close_price']
        print (company, price)
        # make api call to determine current ask price
        company_df, e = get_stock_df(company)
        last_price = company_df.loc[0,'last']
        # check if current ask price is within a tolerance range of the modeled closing price
        h = row['hurdle_price']
        print (h)


if __name__ == '__main__':
    main()