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

notes = input('Enter any notes:\n')
# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)

log_dir = '../ML_logs/'
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

df_file = '../nope_dataframes/combined_tensor_df.csv'
df = pd.read_csv(df_file, compression = 'gzip')

df = df.apply(pd.to_numeric, errors='coerce')
df = df.dropna(axis=1, how='all')

df['buy'] = (df['label'] > .02) * 1
raw_count = df['buy'].sum()
total_population = df.shape[0]

print (df.head())
print (df.shape)

label = 'buy'

train_dataset = df.sample(frac=0.8,random_state=0)
test_dataset = df.drop(train_dataset.index)
test_dataset.to_csv('../ML_logs/test_dataset.csv', compression = 'gzip', index = False)

train_dataset.pop('label')
test_dataset.pop('label')

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
print ('Final train_dataset shape: ', train_dataset.shape)

def norm(x):
    return (x - train_stats['mean']) / train_stats['std']


normed_train_data = norm(train_dataset)
normed_train_data.fillna(0, inplace=True)

normed_test_data = norm(test_dataset)
normed_test_data.fillna(0, inplace=True)
print (normed_train_data.tail())
learning_rate = .000001
clipnorm = 1.

def build_model():
    model = keras.Sequential([
        layers.Dense(128, activation=tf.nn.tanh, input_shape=[len(train_dataset.keys())]),
        layers.Dense(128, activation=tf.nn.tanh),
        layers.Dropout(.1, noise_shape=None, seed=1),
        layers.Dense(64, activation=tf.nn.tanh),
        layers.Dense(64, activation=tf.nn.tanh),
        layers.Dropout(.1, noise_shape=None, seed=1),
        layers.Dense(64, activation=tf.nn.tanh),
        layers.Dense(64, activation=tf.nn.tanh),
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

EPOCHS = 500

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
print (f'raw_count: {raw_count} of {total_population} ({pct_count}')

print('\n\n\n')
print ('test predictions:')
test_predictions = model.predict(normed_test_data)
test_predictions = (test_predictions > .5)
print ('confusion matrix:')
conf_matrix = tf.math.confusion_matrix(test_labels, test_predictions)
print (conf_matrix)
try:
    print (conf_matrix[:][1])
except Exception as e:
    print (str(e))

now_str = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d_%H.%M")
log_file = f'{log_dir}/log_{now_str} - {round(history.history["val_mse"][-1],2)}.txt'
## Save entire model to a HDF5 file
model.save(f'{log_dir}mlearn_{now_str}.h5')
a = str(summary)
str =   notes + \
        '\n\n\n' + \
        'learning rate: {0}\n'.format(learning_rate) + \
        'clipnorm: {0}\n\n'.format(clipnorm) + \
        '{}'.format(hist.tail())

print (str)

# "Loss"
plt.plot(history.history['mse'])
plt.plot(history.history['val_mse'])
plt.title('mse')
plt.ylabel('model mse')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.axhline(y=var)
plt.savefig(f'{log_dir}{now_str}.png')
plt.show()




with open(log_file, 'w') as f:
    f.write(str)

with open(log_file, 'a') as f:
    with redirect_stdout(f):
        model.summary()
