from nope import run_nope
from yf_merge import yf_merge
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-d', '--date_to_run',
                        help='Enter -d 2021-02-24_09.45',
                        required=False)
    args = vars(parser.parse_args())

    if args['date_to_run'] != None:
        print(args)
        run_nope(date_to_run=args['date_to_run'])
        yf_merge(date_to_run=args['date_to_run'])
    else:
        print(args)
        run_nope()
        yf_merge()
