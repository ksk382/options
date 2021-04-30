import matplotlib
import matplotlib.pyplot as plt
from tensorflow.keras.layers.experimental import preprocessing
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
import datetime as dt
from contextlib import redirect_stdout
import os
import time
from run_model_test import run_model_test
import argparse


def mlearn(hurdle, df):
    EPOCHS = 200
    learning_rate = .000005

    # Make numpy values easier to read.
    np.set_printoptions(precision=3, suppress=True)

    log_dir = '../ML_logs/'
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    #df_file = '../nope_dataframes/combined_tensor_df.csv'
    #df = pd.read_csv(df_file, compression = 'gzip')

    # add the labels
    df['buy'] = (df['mvmnt'] > hurdle) * 1
    label = 'buy'
    raw_count = df['buy'].sum()
    total_population = df.shape[0]


    ## slice off and save the test dataset
    train_dataset = df.sample(frac=0.8,random_state=0)
    test_dataset = df.drop(train_dataset.index)
    test_dataset.to_csv('../ML_content/test_dataset.csv', compression = 'gzip', index = False)

    # drop the columns that give away the answer
    train_labels = train_dataset.pop(label)
    test_labels = test_dataset.pop(label)
    dropcols = ['symbol',
                'mvmnt',
                'tmrw_opn',
                'latestPrice',
                'z_date',
                'df_date_x',
                'df_date_y']
    for i in dropcols:
        train_dataset.pop(i)
        test_dataset.pop(i)

    # remove non-numeric columns
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna(axis=1, how='all')


    #sns.pairplot(train_dataset[['days_before_dividend',
    #            'delta_open', 'delta_close', 'delta_high', 'delta_low',
    #            'delta_volume', 'op_1.0']], diag_kind='kde')
    #plt.show()

    # norm the training data, save the norm stats
    train_stats = train_dataset.describe()
    train_stats = train_stats.transpose()
    train_stats.to_csv('../ML_content/train_stats.csv', compression = 'gzip', index = True)

    def norm(x):
        return (x - train_stats['mean']) / train_stats['std']

    normed_train_data = norm(train_dataset)
    normed_train_data.fillna(0, inplace=True)
    normed_test_data = norm(test_dataset)
    normed_test_data.fillna(0, inplace=True)

    final_cols = pd.DataFrame(normed_train_data.columns)
    final_cols.to_csv('../ML_content/final_cols.csv', compression='gzip', index=False)

    def build_model():
        model = keras.Sequential([
            layers.Dense(128, activation=tf.nn.tanh, input_shape=[len(normed_train_data.keys())]),
            layers.Dense(128, activation=tf.nn.tanh),
            layers.Dense(128, activation=tf.nn.tanh),
            layers.Dense(64, activation=tf.nn.tanh),
            layers.Dropout(.2, noise_shape=None, seed=1),
            layers.Dense(64, activation=tf.nn.tanh),
            layers.Dense(64, activation=tf.nn.tanh),
            layers.Dropout(.2, noise_shape=None, seed=1),
            layers.Dense(64, activation=tf.nn.tanh),
            layers.Dense(64, activation=tf.nn.tanh),
            layers.Dropout(.2, noise_shape=None, seed=1),
            layers.Dense(64, activation=tf.nn.tanh),
            layers.Dense(1)
        ])

        optimizer = tf.keras.optimizers.RMSprop(learning_rate)

        model.compile(loss='binary_crossentropy',
                      optimizer=optimizer,
                      metrics=['mae', 'mse', 'accuracy'])
        return model

    model = build_model()
    print (model.summary())
    summary = model.summary()
    #example_batch = normed_train_data[:10]
    #example_result = model.predict(example_batch)
    #print (example_result)

    # Display training progress by printing a single dot for each completed epoch
    class PrintDot(keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs):
            if epoch % 100 == 0: print('')
            print('.', end='')



    #checkpoint_path = "database/cp.ckpt"
    #checkpoint_dir = os.path.dirname(checkpoint_path)

    history = model.fit(
        normed_train_data, train_labels,
        epochs=EPOCHS, validation_split = 0.2,
        callbacks=[PrintDot()])

    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch
    print ('\n\n')
    print (hist.tail())

    var = df[label].std() ** 2
    print ('\npopulation stats:')
    print ('mean: {0}'.format(df[label].mean()))
    print ('std: {0}'.format(df[label].std()))
    print ('std sqd: {0}'.format(var))
    print ('mad: {0}'.format(df[label].mad()))
    pct_count = raw_count / total_population
    print (f'raw_count: {raw_count} of {total_population} ({pct_count})')

    print('\n\n\n')
    print ('test predictions:')
    test_predictions = model.predict(normed_test_data)
    test_predictions = (test_predictions > .5)

    conf_matrix = tf.math.confusion_matrix(test_labels, test_predictions)
    conf_matrix = conf_matrix.numpy()
    pos_rate = conf_matrix[0][1] / (conf_matrix[:,1].sum())
    betting_rate = conf_matrix[:,1].sum() / conf_matrix[:,0].sum()

    test_rate = run_model_test(model, hurdle)

    notes2 = f'data shape: {normed_test_data.shape}\n' + \
            f'hurdle: {hurdle}\n' + \
            f'learning rate: {learning_rate}\n' + \
            f'epochs: {EPOCHS}\n' + \
            f'projected rate of return: {test_rate} \n\n' + \
            f'conf matrix: \n' + \
            f'{conf_matrix} \n' + \
            f'num positive predictions: {conf_matrix[:, 1].sum()}\n' + \
            f'rate of false positives / total positives: {pos_rate}\n' + \
            f'rate of positive prediction (betting rate): {betting_rate})\n\n\n' + \
            '\npopulation stats:\n' + \
            f'mean: {df[label].mean()}\n' + \
            f'std: {df[label].std()}\n' + \
            f'std sqd: {var}\n' + \
            f'mad: {df[label].mad()}\n' + \
            f'raw_count: {raw_count} of {total_population} ({pct_count})\n\n\n'
    print (notes2)

    now_str = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d_%H.%M")
    ## Save entire model to a HDF5 file

    save_name = f'{now_str}_mse_{round(history.history["val_mse"][-1],2)}_return_{test_rate}_h_{hurdle}'
    model.save(f'{log_dir}{save_name}_model.h5')

    # save log file
    log_file = f'{log_dir}{save_name}_log.txt'

    str =   notes2 + '\n\n\n' + \
            f'{hist.tail()}\n\n\n'

    str = str + '\nFinal Columns: \n' + ''.join((e + ', ') for e in normed_train_data.columns)
    print (str)


    # "Loss"
    plt.plot(history.history['mse'])
    plt.plot(history.history['val_mse'])
    plt.title('mse')
    plt.ylabel('model mse')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.axhline(y=var)
    plt.savefig(f'{log_dir}{save_name}_graph.png')
    #plt.show()
    plt.clf()

    with open(log_file, 'w') as f:
        f.write(str)

    with open(log_file, 'a') as f:
        with redirect_stdout(f):
            model.summary()

def run_loop():
    df_file = '../ML_content/combined_tensor_df.csv'
    df = pd.read_csv(df_file, compression='gzip')

    df1 = df.sort_values(by='mvmnt')
    x = pd.qcut(df1['mvmnt'], 20)
    y = []
    for i in x.unique():
        print(i, i.left, i.right)
        y.append(i.right)
    hurdles = y[-6:-2]
    hurdles = list(reversed(hurdles))
    print(f'hurdles: {hurdles}')
    input('enter')
    for hurdle in hurdles:
        mlearn(hurdle, df)

def run_one(h):
    '''df_file = '../nope_dataframes/combined_tensor_df.csv'
    df = pd.read_csv(df_file, compression='gzip')

    df1 = df.sort_values(by='mvmnt')
    x = pd.qcut(df1['mvmnt'], 10)
    y = []
    for i in x.unique():
        print(i, i.left, i.right)
        y.append(i.right)
    hurdles = y[2:-1]

    hurdle = hurdles[-1]'''
    df_file = '../ML_content/combined_tensor_df.csv'
    df = pd.read_csv(df_file, compression='gzip')
    hurdle = float(h)
    notes = f'trying with high hurdle: {hurdle}'
    print(notes)

    mlearn(hurdle, df)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-j', '--hurdle',
                        help='Enter -j .015',
                        required=False)
    args = vars(parser.parse_args())

    if args['hurdle'] != None:
        h = args['hurdle']
        run_one(h)
    else:
        run_loop()
