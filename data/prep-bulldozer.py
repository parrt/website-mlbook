# Data must be logged in to get. Download Train.zip from:
# https://www.kaggle.com/c/bluebook-for-bulldozers/data
# Uncompress to get Train.csv, then run this program in same dir as that Train.csv
# to get bulldozer-train.feature which is much faster to load.
# python prep-bulldozer.py 

import pandas as pd
import csv
import os


if not os.path.isfile('Train.csv'):
    print("Can't find Train.csv file; must execute this program in same dir")
    print("To get Train.csv, go to https://www.kaggle.com/c/bluebook-for-bulldozers/data")
    exit()

dtypes = {col:str for col in ['fiModelSeries', 'Coupler_System', 'Grouser_Tracks', 'Hydraulics_Flow']}
df = pd.read_csv("bulldozer-train.csv", dtype=dtypes, parse_dates=['saledate']) # 35s load
df = df.sort_values('saledate')
df = df.reset_index(drop=True)

n_valid = 12000  # same as Kaggle's test set size
n_train = len(df)-n_valid
df_train = df[:n_train].reset_index(drop=True)
df_valid = df[n_train:].reset_index(drop=True)
df_train.to_feather("bulldozer-train.feather")
print("Created bulldozer-train.feather")
df_valid.to_feather("bulldozer-valid.feather")
print("Created bulldozer-valid.feather")
