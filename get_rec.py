# -*- coding: utf-8 -*-
import pandas as pd
import os
from tensorflow.keras.models import load_model
pd.options.mode.chained_assignment = None



train_stats = pd.read_csv('../ML_logs/train_stats.csv', compression = 'gzip')
train_stats = train_stats.set_index('Unnamed: 0')

final_cols = pd.read_csv('../ML_logs/final_cols.csv', compression='gzip')
cols = list(final_cols['0'])

model_path = '../ML_logs/'

try:
    model_file = sorted([(model_path + i) for i in os.listdir(model_path) if i.endswith('_primary.h5')])[0]
except:

    list_of_models = [(model_path + i) for i in os.listdir(model_path) if i.endswith('.h5')]
    #print (list_of_models)
    model_file = max(list_of_models, key=os.path.getctime)

print(f'loading model: {model_file}')
model = load_model(model_file)

def norm(x):
    return (x - train_stats['mean']) / train_stats['std']

def get_rec(tensor_df):
    cols = list(final_cols['0'])
    x = tensor_df[cols]
    x = x.apply(pd.to_numeric, errors='coerce')
    x = x.dropna(axis=1, how='all')
    x = norm(x)
    x.fillna(0, inplace=True)
    test_predictions = model.predict(x)
    rec = tensor_df[['symbol','name_y','cl_s_y']]
    rec['pred'] = test_predictions
    rec['buy'] = (rec['pred'] > .5) * 1
    return rec
