# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from build_tensors import make_rec_tensors
import os
from tensorflow.keras.models import load_model
pd.options.mode.chained_assignment = None



model_path = '../ML_logs/'

try:
    model_file = sorted([(model_path + i) for i in os.listdir(model_path) if i.endswith('_primary.h5')])[0]
except:
    list_of_models = [(model_path + i) for i in os.listdir(model_path) if i.endswith('.h5')]
    #print (list_of_models)
    model_file = max(list_of_models, key=os.path.getctime)
    hurdle = float(model_file.split('_')[-1].replace('.h5',''))

print(f'loading model: {model_file}')

model = load_model(model_file)

def norm(x):
    train_stats = pd.read_csv('../ML_logs/train_stats.csv', compression='gzip')
    train_stats = train_stats.set_index('Unnamed: 0')
    return (x - train_stats['mean']) / train_stats['std']

def get_rec(tensor_df):

    final_cols = pd.read_csv('../ML_logs/final_cols.csv', compression='gzip')
    cols = list(final_cols['0'])
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

def make_recs(now_str):
    pd.set_option('display.max_rows', 800)
    pd.set_option('display.min_rows', 200)

    today_stock_file = f'../stock_dataframes/{now_str}_synth.csv'
    df2 = pd.read_csv(today_stock_file, compression='gzip')

    pr_date = df2['pr_date'].head(1).item()
    stock_df_list = [i for i in os.listdir('../stock_dataframes/') if (i.endswith('_synth.csv') and pr_date in i)]
    stock_df_name = sorted(stock_df_list)[0]

    yesterday_stock_file = f'../stock_dataframes/{stock_df_name}'
    df1 = pd.read_csv(yesterday_stock_file, compression='gzip')

    today_nope = f'../nope_dataframes/{now_str}_nope.csv'
    nope_df = pd.read_csv(today_nope, compression='gzip')
    nope_df['symbol'] = nope_df['ticker']

    sp_500_df = pd.read_csv('sp500_ticker_list.csv', compression='gzip')
    etf_df = pd.read_csv('etf_ticker_list.csv', compression='gzip')

    df = make_rec_tensors(df1, df2, nope_df, sp_500_df, etf_df)
    rec_df = get_rec(df)
    rec_df = rec_df.round(3)
    pre_screen_length = rec_df[rec_df['buy']==1].index
    print (f'pre-screen list: {len(pre_screen_length)}')
    no_go_df = pd.read_csv('../no_go.csv')
    x = no_go_df[no_go_df['exclude'] == 1]['Ticker']
    y = rec_df[rec_df['symbol'].isin(x)].index
    rec_df = rec_df.drop(rec_df.index[y])
    rec_df = rec_df.sort_values(by='confidence', ascending=False)
    rec_df.to_csv(f'../nope_dataframes/recs_{now_str}.csv', compression='gzip', index=False)
    print ('\n\n')
    return rec_df


if __name__ == "__main__":
    #now_str = '2021-02-11_15.00'
    s_dir = '../stock_dataframes/'
    list_of_files = [(s_dir + i) for i in os.listdir(s_dir) if (i.endswith('_synth.csv'))]
    stock_df_name = max(list_of_files, key=os.path.getctime)
    time_str = stock_df_name.replace(s_dir, '').replace('_synth.csv', '')
    print (time_str)
    rec_df = make_recs(time_str)
    y = rec_df[rec_df['buy'] == 1]
    print(y)
    print(len(y.index))
    #print(y['symbol'].unique())


