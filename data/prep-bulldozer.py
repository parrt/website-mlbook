# Data must be logged in to get. Download Train.zip from:
# https://www.kaggle.com/c/bluebook-for-bulldozers/data
# Uncompress to get Train.csv, then run this program in same dir as that Train.csv
# to get bulldozer-train.feature which is much faster to load.
# python prep-bulldozer.py 

import pandas as pd
import csv
import os


if not (os.path.isfile('Train.csv') and os.path.isfile('Valid.csv') and os.path.isfile('ValidSolution.csv')):
    print("Can't find Train.csv or Valid.csv or ValidSolution.csv file; must execute this program in same dir")
    print("To get these files, go to https://www.kaggle.com/c/bluebook-for-bulldozers/data")
    exit()

dtypes = {col:str for col in ['fiModelSeries', 'Coupler_System', 'Grouser_Tracks', 'Hydraulics_Flow']}
df = pd.read_csv('Train.csv', dtype=dtypes, parse_dates=['saledate']) # 35s load
df = df.sort_values('saledate')
df = df.reset_index(drop=True)

df.to_feather("bulldozer-train-all.feather")
print("Created bulldozer-train-all.feather")

# Split out validation set and make training/validation sets
n_valid = 12000  # same as Kaggle's test set size
n_train = len(df)-n_valid
df_train = df[:n_train].reset_index(drop=True)
df_valid = df[n_train:].reset_index(drop=True)
df_train.to_feather("bulldozer-train.feather")
print("Created bulldozer-train.feather")
df_valid.to_feather("bulldozer-valid.feather")
print("Created bulldozer-valid.feather")

# Read Kaggle validation / solution and make it our test set
df_test = pd.read_csv("Valid.csv", dtype=dtypes, parse_dates=['saledate'])
df_test = df_test.sort_values('saledate')
df_test_soln = pd.read_csv("ValidSolution.csv")
df_test_soln['SalePrice'] = df_test_soln['SalePrice'].astype(int)
del df_test_soln['Usage']
df_merged = df_test.merge(df_test_soln, on='SalesID', how='left') # merge in solution
df_merged.to_feather("bulldozer-test.feather")
print("Created bulldozer-test.feather")
