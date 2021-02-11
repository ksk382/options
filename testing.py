from gather import load_ticker_list
import pandas as pd
import numpy as np

no_go_list = pd.read_csv('../no_go.csv')
df = load_ticker_list()


keys = list(no_go_list.columns.values)
i1 = df.set_index(keys).index
i2 = no_go_list.set_index(keys).index
y = df[~i1.isin(i2)]

print (y)