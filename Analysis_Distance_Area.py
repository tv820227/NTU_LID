#%%
# import modules
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# change working directory
path = "C:\\TV\\Results\\OptimalResult\\Result"
os.chdir(path)

# get data from .txt and change into DataFrame
from glob import glob
file_list = glob('*.txt')
df_list = []
for file in file_list:
    df = pd.read_csv(file, skiprows=1, header=0, sep="\t")
    df = df[['Subcatchment', 'Bio_Area', 'Pav_Area']]
    df.columns = ['Sub', 'Bio_Area', 'Pav_Area']
    drop_index = list(df.index)[-4:]
    df = df.drop(drop_index)
    df_list.append(df)

# read the file which store the relationship between subcatchment and length to out fall B
len_file_path = "C:\\TV\\Results\\Out_Length.csv"
length = pd.read_csv(len_file_path, header=0)
length = length[['Sub', 'Out_Length']]
