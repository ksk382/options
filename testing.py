# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
import seaborn as sns
import os


pr_date = '2021-02-08'
stock_df_list = [i for i in os.listdir('../stock_dataframes/') if (i.endswith('_synth.csv') and pr_date in i)]
stock_df_name = sorted(stock_df_list)[0]
print (stock_df_list)
print (stock_df_name)