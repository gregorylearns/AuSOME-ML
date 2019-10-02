import pandas as pd

file = pd.read_csv('HSC20_D_Channel4_DATA4.csv')
file = file.drop(['Unnamed: 0'], axis=1)

file.to_csv('Channel3_Data.csv', index=False)