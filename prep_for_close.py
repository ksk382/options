from nope import run_nope
from clean_up import clean_up
from ohlcv_retrieve import yf_ohlcv

if __name__=='__main__':
    x = run_nope()
    if x = 1:
        yf_ohlcv()
        clean_up()
        print (f'\n\n\n\n&&&&&----- Nope, ohlcv, and clean_up complete')
    else:
        print ('nope did not complete')