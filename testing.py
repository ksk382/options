from tensor_time import munge
import pandas as pd
import datetime as dt
import os
from create_combined_dfs import latest_file
from tensorflow.keras.models import load_model
import tensorflow as tf



def get_rec(tensor_df, m, cols, train_stats):

    def norm(x):
        return (x - train_stats['mean']) / train_stats['std']

    model = load_model(m)
    hurdle = float(m.split('_')[-1].replace('.h5', ''))
    x = tensor_df[cols]
    x = x.apply(pd.to_numeric, errors='coerce')
    x = x.dropna(axis=1, how='all')
    x = norm(x)
    x.fillna(0, inplace=True)
    test_predictions = model.predict(x)
    rec = tensor_df[['symbol','name_y','cl_s_y']]
    rec.columns = ['symbol','name','close_price']
    rec['hurdle'] = hurdle
    rec['hurdle_price'] = rec['close_price'] + rec['close_price'] * rec['hurdle']
    rec['hurdle_price'] = rec['hurdle_price'].round(2)
    rec['confidence'] = test_predictions
    rec['buy'] = (rec['confidence'] > .5) * 1
    return rec


def main():
    now = dt.datetime.now()
    now_str = dt.datetime.strftime(now, "%Y-%m-%d_%H.%M")
    print(now_str)
    today_str = dt.datetime.strftime(now, "%Y-%m-%d")

    #run checks
    '''
    check whether the data for the day exists
    get account cash amount
    '''




    # load df1 and df2 (combined dataframes from today and yesterday)
    x_date = '2021-04-13'
    y_date = '2021-04-14'
    df1 = pd.read_csv(f'../combined_dataframes/{x_date}.csv', compression='gzip')
    df2 = pd.read_csv(f'../combined_dataframes/{y_date}.csv', compression='gzip')
    quote_df_name = latest_file('../quote_dataframes/', y_date)
    quote_df = pd.read_csv(quote_df_name, compression='gzip')
    print(f'initial_shapes--    df1: {df1.shape}    df2: {df2.shape}   quote_df: {quote_df.shape}')
    df3 = munge(df1, df2, quote_df)
    print (df3.tail())

    final_cols = pd.read_csv('../ML_content/final_cols.csv', compression='gzip')
    final_cols = list(final_cols['0'])
    df4 = df3[final_cols]

    print (df4.tail())

    train_stats = pd.read_csv('../ML_content/train_stats.csv', compression='gzip', index_col = 0)

    # load model
    model_file = '../ML_logs/2021-04-14_17.49 - hurdle - 0.0218 mse - 0.09 test_rate - 0.0456_model_0.0218.h5'

    r = get_rec(df4, model_file, final_cols, train_stats)

    print (r)


    # should the ticker list be shuffled? otherwise you always buy early on
    # large cap
    # for each ticker,
    #   pull a live quote

    # updated thought 4.10.21: if you're firing live like that, you don't
    # know what percentage of capital to throw at it. I.e. need all the buys
    # before you can estimate buy amounts

    #   merge the data into a tensor
    #   munge(df1, df2, quote_df)
    #   strip out the columns not used in the model
    #   normalize the data to the train norms
    #   push the tensor through the model to get a buy decision

    #   execute a buy decision
    #   log the buys

    return

if __name__ == '__main__':
    main()