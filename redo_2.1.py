import os
import pandas as pd

odir = '../option_dataframes/2021-02-01/'
x = os.listdir(odir)

ticker_df = pd.read_csv('IWV_holdings.csv')
ticker_list = list(ticker_df['Ticker'].unique())
etf_df = pd.read_csv('etf_ticker_list.csv')
ticker_list = ticker_list + list(etf_df['Ticker'].unique())

option_dir_name = '../option_dataframes/2021-02-01_15.30/'
if not os.path.exists(option_dir_name):
    os.mkdir(option_dir_name)

for ticker in ticker_list:
    files = [(option_dir_name + i) for i in x if i.startswith(ticker)]
    latest_file = max(files, key=os.path.getctime)
    new_name = option_dir_name + ticker + '_.csv'
    os.rename(latest_file, new_name)
    print (new_name)