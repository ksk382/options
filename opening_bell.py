from nope import run_nope
from yf_retrieve import yf_ohlcv, clear_ohlcv
from yf_merge import make_today_frame
import datetime as dt
from time_to_sell import sell_all

if __name__=='__main__':
    #sell_all()
    clear_ohlcv()
    print ('cleared ohlcv folder')
    yf_ohlcv()
    print ('done with yf_ohlcv')
    print ('making today frame')
    make_today_frame()

