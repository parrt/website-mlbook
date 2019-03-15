# Data must be logged in to get
# https://www.kaggle.com/c/two-sigma-connect-rental-listing-inquiries/download/train.json
# Then run this program in same dir as that train.json data to get csv; e.g.,
# python prep-rent.py 
# which creates rent.csv and rent-ideal.csv

import pandas as pd
import csv
import os


if not os.path.isfile('train.json'):
    print("Can't find train.json file; must execute this program in same dir")
    print("To get train.json, go to https://www.kaggle.com/c/two-sigma-connect-rental-listing-inquiries/data")
    exit()

df = pd.read_json('train.json')

# Create csv from json
df.to_csv("rent.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)
print("Created rent.csv")

# Create ideal numeric data set
df = df[(df.price>1_000) & (df.price<10_000)]
df = df[(df.longitude!=0) | (df.latitude!=0)]
df = df[(df['latitude']>40.55) & (df['latitude']<40.94) &
        (df['longitude']>-74.1) & (df['longitude']<-73.67)]
df_num = df[['bedrooms','bathrooms','latitude','longitude','price']]
df_num.to_csv("rent-ideal.csv", index=False)
print("Created rent-ideal.csv")
