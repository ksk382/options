# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
import seaborn as sns
import os

save_path = '../ohlcv/'
if not os.path.exists(save_path):
    print('path doesnt exist')


x = [(save_path + i) for i in os.listdir(save_path) if i.endswith('.csv')]
for i in x:
    print (i)
    os.remove(i)