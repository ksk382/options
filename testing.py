import yfinance as yf
import json
import pandas as pd
from nonroutine.black_scholes import BSMerton

pd.set_option('display.max_rows', 800)
pd.set_option('display.min_rows', 200)
ticker = 'MSFT'
df1 = pd.read_csv(f'../option_dataframes/2021-02-11_09.45/{ticker}_.csv', compression = 'gzip')
df2 = pd.read_csv(f'../option_dataframes/2021-02-11_15.00/{ticker}_.csv', compression = 'gzip')
sdf = pd.read_csv('../stock_dataframes/2021-02-11_09.45_synth.csv', compression = 'gzip')
print (df)
print (df.loc[0])
print (sdf)
print (sdf.loc[0])
