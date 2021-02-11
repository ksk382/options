from nope import run_nope
from clean_up import clean_up
from ohlcv_retrieve import yf_ohlcv, clear_ohlcv
import datetime as dt

if __name__=='__main__':
    clear_ohlcv()
    yf_ohlcv()
    clean_up()
