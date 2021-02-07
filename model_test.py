# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import os
from tensorflow.keras.models import load_model
import tensorflow as tf

def model_test():
    pd.set_option('display.max_rows', 2000)
    pd.set_option('display.min_rows', 100)

    model_path = '../ML_logs/'
    list_of_models = [(model_path + i) for i in os.listdir(model_path) if i.endswith('.h5')]
    #print (list_of_models)
    latest_file = max(list_of_models, key=os.path.getctime)
    print(latest_file)
    hurdle = float(latest_file.split('_')[-1].replace('.h5',''))

    train_stats = pd.read_csv('../ML_logs/train_stats.csv', compression = 'gzip')
    train_stats = train_stats.set_index('Unnamed: 0')
    print (train_stats.shape)

    test_dataset = pd.read_csv('../ML_logs/test_dataset.csv', compression = 'gzip')

    def norm(x):
        return (x - train_stats['mean']) / train_stats['std']

    test_labels = (test_dataset['mvmnt'] > hurdle) * 1
    true_label = test_dataset.pop('mvmnt')
    test_dataset.pop('buy')

    print(test_dataset.shape)
    print (test_dataset.columns)
    normed_test_data = norm(test_dataset)
    normed_test_data.fillna(0, inplace=True)

    model = load_model(latest_file)
    test_predictions = model.predict(normed_test_data)
    binary_test_pred = (test_predictions > .5) * 1
    test_dataset['binary_test_pred'] = binary_test_pred
    test_dataset['test_pred'] = test_predictions
    test_dataset['true_label'] = true_label
    test_dataset['profit'] = test_dataset['binary_test_pred'] * test_dataset['true_label']
    cols = ['test_pred', 'binary_test_pred', 'true_label', 'profit']
    test_dataset = test_dataset.sort_values(by='profit', ascending=False)
    test_dataset = test_dataset.round(4)
    #print (test_dataset[cols])
    r = test_dataset['profit'].sum() / test_dataset['binary_test_pred'].sum()
    r = round(r,4)
    num_bets = test_dataset['binary_test_pred'].sum()

    print (normed_test_data.shape)
    conf_matrix = tf.math.confusion_matrix(test_labels, binary_test_pred)
    pos = conf_matrix.numpy()
    print (pos)
    pos_rate = pos[0][1] / (pos[:,1].sum())
    print (f'rate of false positives / total positives: {pos_rate}')
    print (f'number of bets: {num_bets}')
    print (f'rate of return: {r}')
    return r

if __name__=='__main__':
    model_test()

