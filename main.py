from gather import gather_stock_and_option_data
from nope import run_nope
from clean_up import clean_up
from ohlcv_retrieve import yf_ohlcv

if __name__=='__main__':
    now_str = gather_stock_and_option_data()
    run_nope(date_to_run=now_str)
    yf_ohlcv()
    clean_up(date_to_run=now_str)


