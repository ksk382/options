from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())
import os
import datetime as dt
import pandas as pd
import requests

pd.set_option('display.max_rows', 500)

'''
now = dt.datetime.now()
today_str = dt.datetime.strftime(now, "%Y-%m-%d")

rec_path = '../recs/'
start_string = rec_path + f'recs_{today_str}'
flist = [(rec_path + i) for i in os.listdir(rec_path) if i.endswith('.csv') and i.startswith(start_string)]

try:
    latest_file = max(flist, key=os.path.getctime)
    print (latest_file)
except:
    print ('no rec file found for today...exiting')
    sys.exit()

df = pd.read_csv(latest_file, compression='gzip')
print (df)'''

now = dt.datetime.now()

rec_dir = '../recs/'
rec_files = os.listdir(rec_dir)
rec_files = sorted([i for i in rec_files if i.endswith('.csv') and i.startswith('rec_')], reverse=True)
for i in rec_files:
    print (i)
    rec_file = rec_dir + i
    df = pd.read_csv(rec_file, compression='gzip')
    date_y = df.iloc[0]['df_date_y']
    d = pd.to_datetime(date_y)
    print (d)

    next_day = d + dt.timedelta(days = 1)
    next_day_file = '../quote_dataframes/' + dt.datetime.strftime(next_day, "%Y-%m-%d") + '_09.50.csv'
    if not os.path.exists(next_day_file):
        print (f'no next day file {next_day_file}')
        continue
    print (next_day_file)
    df2 = pd.read_csv(next_day_file, compression='gzip')
    # print (df2)
    df2['today_price'] = df2['latestPrice']
    df2 = df2[['symbol', 'today_price']]
    df3 = pd.merge(df, df2, on='symbol')
    df3['profit'] = (df3['today_price'] - df3['latestPrice']) / df3['latestPrice']

    print(df3)
    print(df3['profit'].mean())

    input('enter')

