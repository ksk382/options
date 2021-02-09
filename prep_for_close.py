from nope import run_nope
from clean_up import clean_up
from ohlcv_retrieve import yf_ohlcv, clear_ohlcv

if __name__=='__main__':
    x = run_nope(date_to_run='2021-02-09_15.00')
    if x == 1:
        #clear_ohlcv()
        yf_ohlcv()
        clean_up()
        print (f'\n\n\n\n&&&&&----- Nope, ohlcv, and clean_up complete')
    else:
        print ('nope did not complete')