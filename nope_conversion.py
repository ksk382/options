import os
import pandas as pd


third_dir = '../nope_dataframes/'
flist = [(third_dir + i) for i in os.listdir(third_dir) if i.endswith('_nope.csv')]
for i in flist:
    df = pd.read_csv(i, compression = 'gzip')
    df = df.rename({'ticker': 'symbol'}, axis=1)
    df.to_csv(i, compression='gzip', index=False)
    print (i)
print('done')
