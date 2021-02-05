# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import os
from tensorflow.keras.models import load_model
import tensorflow as tf

pd.set_option('display.max_rows', 2000)
pd.set_option('display.min_rows', 1100)

model_path = '../ML_logs/'
list_of_models = [(model_path + i) for i in os.listdir(model_path) if i.endswith('.h5')]
#print (list_of_models)
latest_file = max(list_of_models, key=os.path.getctime)
print(latest_file)

train_stats = pd.read_csv('../ML_logs/train_stats.csv', compression = 'gzip')
train_stats = train_stats.set_index('Unnamed: 0')

test_dataset = pd.read_csv('../ML_logs/test_dataset.csv', compression = 'gzip')

def norm(x):
    return (x - train_stats['mean']) / train_stats['std']

test_labels = (test_dataset['mvmnt'] > .0075) * 1
true_label = test_dataset.pop('mvmnt')
test_dataset.pop('buy')

normed_test_data = norm(test_dataset)
normed_test_data.fillna(0, inplace=True)

model = load_model(latest_file)
print ('test predictions:')
test_predictions = model.predict(normed_test_data)
binary_test_pred = (test_predictions > .5) * 1
print (test_predictions)
test_dataset['binary_test_pred'] = binary_test_pred
test_dataset['test_pred'] = test_predictions
test_dataset['true_label'] = true_label
test_dataset['profit'] = test_dataset['binary_test_pred'] * test_dataset['true_label']
cols = ['test_pred', 'binary_test_pred', 'true_label', 'profit']
test_dataset = test_dataset.sort_values(by='profit')
print (test_dataset[cols].tail())
r = test_dataset['profit'].sum() / test_dataset['binary_test_pred'].sum()
num_bets = test_dataset['binary_test_pred'].sum()

print (f'rate of return: {round(r,4)}')
print (f'number of bets: {num_bets}')

conf_matrix = tf.math.confusion_matrix(test_labels, binary_test_pred)
print (conf_matrix)
