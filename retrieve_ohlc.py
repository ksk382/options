import datetime as dt
import sys
import os
import pandas as pd
import yfinance as yf
from pathlib import Path
from gather import load_ticker_list

def yf_ohlcv(ticker_list):

    today = dt.datetime.now()
    # 253 trading days in a year
    days_back = 20
    DD = dt.timedelta(days=days_back)
    earlier = today - DD
    earlier_str = earlier.strftime("%Y-%m-%d")
    today_str = today.strftime("%Y-%m-%d")

    save_path = '../ohlcv/'
    if os.path.exists(save_path):
        print('path exists')
    else:
        os.mkdir(save_path)

    count = 0
    for ticker in ticker_list:
        count +=1
        f_name = f'{save_path}{ticker}.csv'
        if os.path.isfile(f_name):
            print (f'{count} - {ticker} -- exists')
        else:
            print (f'{count} out of {len(ticker_list)} - {ticker}')
            y = yf.download(ticker, start=earlier_str, end=today_str,
                            group_by="ticker")
            x = pd.DataFrame(y)
            x['Date'] = x.index
            x.to_csv(f_name, compression='gzip', index=False)
            if count % 50 == 0:
                root_directory = Path(save_path)
                size = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file()) / 1000000
                print (f'size: {size} MB')
                if size > 500:
                    sys.exit(0)
    return

if __name__ == "__main__":
    ticker_list = load_ticker_list()
    yf_ohlcv(ticker_list)