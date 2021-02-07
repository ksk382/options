# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
import seaborn as sns
import os

pd.set_option('display.max_rows', 2000)
pd.set_option('display.min_rows', 200)

np.set_printoptions(precision=3, suppress=True)

log_dir = '../ML_logs/'
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

df_file = '../nope_dataframes/combined_tensor_df.csv'
df = pd.read_csv(df_file, compression = 'gzip')

df = df.apply(pd.to_numeric, errors='coerce')
df = df.dropna(axis=1, how='all')

sns.distplot(df[['mvmnt']], hist=False, rug=True)

df = df.sort_values(by='mvmnt')
print (df)

print (df.describe())

x = pd.qcut(df['mvmnt'], 10)
y = []
for i in x.unique():
    print(i, i.left, i.right)
    y.append(i.right)
hurdles = y[-6:-1]
print (hurdles)

#print (y)

#x = input('plot?')
#if x == 'y':
#    plt.show()