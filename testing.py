# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import requests
from cred_file import *
from io import StringIO
import pandas as pd
import datetime as dt
import os
import time
import numpy as np
import seaborn as sns
import xml.etree.ElementTree as ET
import pandas as pd
import datetime as dt
from cred_file import oauth_hdr, stock_endpoint, option_endpoint
import json
import pprint
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
import datetime as dt
from contextlib import redirect_stdout
import os
from tensorflow.keras.models import load_model


pd.set_option('display.max_rows', 800)
pd.set_option('display.min_rows', 50)

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

true_label = test_dataset.pop('label')
test_dataset.pop('buy')

print (test_dataset.tail())
print (test_dataset.shape)
for i in test_dataset.columns:
    print (i)

normed_test_data = norm(test_dataset)
normed_test_data.fillna(0, inplace=True)
print (normed_test_data.tail(100))

model = load_model(latest_file)
print ('test predictions:')
test_predictions = model.predict(normed_test_data)
test_predictions = (test_predictions > .5) * 1
print (test_predictions)
test_dataset['test_pred'] = test_predictions
test_dataset['true_label'] = true_label
test_dataset['profit'] = test_dataset['test_pred'] * test_dataset['true_label']
cols = ['test_pred', 'true_label']
print (test_dataset[cols])
print (round(test_dataset['profit'].mean(),2))
