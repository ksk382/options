import pandas as pd
import datetime as dt
import os

pd.set_option('display.max_rows', 800)


def latest_file(dir_name, today_str):
    flist = [(dir_name + i) for i in os.listdir(dir_name) if (i.endswith('.csv') and i.startswith(today_str))]
    print (flist)
    fname = max(flist, key=os.path.getctime)
    return fname

first_dir = '../stock_dataframes/'
second_dir = '../stat_dataframes/'
third_dir = '../nope_dataframes/'
out_dir = '../combined_dataframes/'

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

now = dt.datetime.now()
now_str = dt.datetime.strftime(now, "%Y-%m-%d_%H.%M")
print(now_str)

today_str = "2021-04-01"
df1_name = latest_file(first_dir, today_str)
df2_name = latest_file(second_dir, today_str)
df3_name = latest_file(third_dir, today_str)
df1 = pd.read_csv(df1_name, compression = 'gzip')
df2 = pd.read_csv(df2_name, compression = 'gzip')
df3 = pd.read_csv(df3_name, compression = 'gzip')

df4 = pd.merge(df1, df2, on=['symbol'])
print (df4.columns)
df4 = pd.merge(df4, df3, on=['symbol'])
print (df4.columns)

out_name = f'{out_dir}{today_str}.csv'
df4.to_csv(out_name, compression='gzip', index=False)