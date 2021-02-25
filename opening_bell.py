from nope import run_nope
from yf_retrieve import yf_ohlcv, clear_ohlcv, make_today_frame
import datetime as dt

if __name__=='__main__':
    clear_ohlcv()
    print ('cleared ohlcv folder')
    yf_ohlcv()
    print ('done with yf_ohlcv')
    print ('making today frame')
    make_today_frame()

