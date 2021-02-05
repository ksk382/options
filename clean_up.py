import pandas as pd
from gather import load_ticker_list



'''

Need to get clean data that shows day -1 ohlcv, day 0 ohlcv, and day +1 o

'''

pd.set_option('display.min_rows', 50)
pd.set_option('display.max_rows', 200)

ticker_list = load_ticker_list()
o_dir = '../ohlcv/'
s_dir = '../stock_dataframes/'
for ticker in ticker_list[:5]:
    o_name = o_dir + ticker + '.csv'
    o = pd.read_csv(o_name, compression = 'gzip')
    print (o)


