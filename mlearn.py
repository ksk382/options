import matplotlib
matplotlib.use('TkAgg')
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

def mlearn(notes, hurdle, df):
    # Make numpy values easier to read.
    np.set_printoptions(precision=3, suppress=True)

    log_dir = '../ML_logs/'
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    #df_file = '../nope_dataframes/combined_tensor_df.csv'
    #df = pd.read_csv(df_file, compression = 'gzip')

    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna(axis=1, how='all')

    df['buy'] = (df['mvmnt'] > hurdle) * 1
    label = 'buy'
    raw_count = df['buy'].sum()
    print (f'hurdle: {hurdle} -- raw_count: {raw_count}')
    time.sleep(.5)
    total_population = df.shape[0]

    print (df.head())
    print (df.shape)

    train_dataset = df.sample(frac=0.8,random_state=0)
    test_dataset = df.drop(train_dataset.index)
    test_dataset.to_csv('../ML_logs/test_dataset.csv', compression = 'gzip', index = False)

    for i in ['mvmnt']:
        train_dataset.pop(i)
        test_dataset.pop(i)

    #sns.pairplot(train_dataset[['days_before_dividend',
    #            'delta_open', 'delta_close', 'delta_high', 'delta_low',
    #            'delta_volume', 'op_1.0']], diag_kind='kde')

    train_labels = train_dataset.pop(label)
    test_labels = test_dataset.pop(label)
    #plt.show()
    train_stats = train_dataset.describe()
    train_stats = train_stats.transpose()
    train_stats.to_csv('../ML_logs/train_stats.csv', compression = 'gzip', index = True)

    print (train_dataset.tail())
    print (train_dataset.columns)
    final_cols = pd.DataFrame(train_dataset.columns)
    final_cols.to_csv('../ML_logs/final_cols.csv', compression = 'gzip', index = False)
    print ('Final train_dataset shape: ', train_dataset.shape)

    def norm(x):
        return (x - train_stats['mean']) / train_stats['std']


    normed_train_data = norm(train_dataset)
    normed_train_data.fillna(0, inplace=True)

    normed_test_data = norm(test_dataset)
    normed_test_data.fillna(0, inplace=True)
    print (normed_train_data.tail())
    learning_rate = .00001

    def build_model():
        model = keras.Sequential([
            layers.Dense(128, activation=tf.nn.tanh, input_shape=[len(train_dataset.keys())]),
            layers.Dense(128, activation=tf.nn.tanh),
            layers.Dense(128, activation=tf.nn.tanh),
            layers.Dropout(.2, noise_shape=None, seed=1),
            layers.Dense(64, activation=tf.nn.tanh),
            layers.Dense(64, activation=tf.nn.tanh),
            layers.Dropout(.2, noise_shape=None, seed=1),
            layers.Dense(64, activation=tf.nn.tanh),
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

    EPOCHS = 300

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

    print ('confusion matrix:')
    conf_matrix = tf.math.confusion_matrix(test_labels, test_predictions)
    conf_matrix = conf_matrix.numpy()
    print (conf_matrix)
    pos_rate = conf_matrix[0][1] / (conf_matrix[:,1].sum())
    print (f'num positive predictions: {conf_matrix[:,1].sum()}')
    print (f'rate of false positives / total positives: {pos_rate}')

    now_str = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d_%H.%M")
    ## Save entire model to a HDF5 file
    r_ = run_model_test(model, hurdle)
    save_name = f'{now_str} - hurdle - {hurdle} mse - {round(history.history["val_mse"][-1],2)} r_ - {r_}'
    model.save(f'{log_dir}{save_name}_model_{hurdle}.h5')
    # save log file
    log_file_name = f'{log_dir}{save_name}_log'
    log_file = f'{log_file_name}.txt'

    str =   notes + \
            '\n\n\n' + \
            f'hurdle: {hurdle}\n'+ \
            f'learning rate: {learning_rate}\n'+ \
            f'projected rate of return: {r_}\n\n' + \
            f'{conf_matrix} \n' + \
            f'num positive predictions: {conf_matrix[:, 1].sum()}\n' + \
            f'rate of false positives / total positives: {pos_rate}\n\n' + \
            f'{hist.tail()}\n\n\n'

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
    df_file = '../nope_dataframes/combined_tensor_df.csv'
    df = pd.read_csv(df_file, compression='gzip')

    df1 = df.sort_values(by='mvmnt')
    x = pd.qcut(df1['mvmnt'], 10)
    y = []
    for i in x.unique():
        print(i, i.left, i.right)
        y.append(i.right)
    hurdles = y[-4:-1]
    print(hurdles)
    input('enter')
    for hurdle in hurdles:
        notes = f'hurdle: {hurdle}'
        print(notes)
        mlearn(notes, hurdle, df)

def run_one():
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
    df_file = '../nope_dataframes/combined_tensor_df.csv'
    df = pd.read_csv(df_file, compression='gzip')
    hurdle = .0163
    notes = f'trying with high hurdle: {hurdle}'
    print(notes)

    mlearn(notes, hurdle, df)


if __name__ == '__main__':
    run_one()
    #run_loop()