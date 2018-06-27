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
    drop_index = list(df.index)[-4:]
    df = df.drop(drop_index)

    # change column index
    df = df[['Subcatchment', 'Bio_Area', 'Pav_Area']]
    df.columns = ['Sub', 'Bio_Area', 'Pav_Area']
    
    # label rain style into duration and period 
    rain = file.split('-')[0]
    df['duration'] = rain.split('_')[0]
    df['period'] = rain.split('_')[1]

    df_list.append(df)

# read the file which store the relationship between subcatchment and length to out fall B
len_file_path = "C:\\TV\\Results\\Out_Length.csv"
length = pd.read_csv(len_file_path, header=0)
length = length[['Sub', 'Out_Length', 'Area']]

# concate all dataframe through rows and merge Length by 'Sub'
alldf = pd.concat(df_list, axis='rows', ignore_index=True)
alldf = pd.merge(alldf, length, on='Sub')

#%%
alldf['Sub'] = alldf['Sub'].astype('category')
gdf = alldf.groupby('Sub').mean()
gdf['LID_area'] = gdf['Bio_Area'] + gdf['Pav_Area']
gdf['LID_ratio'] = gdf['LID_area']/gdf['Area']*100
gdf = gdf.sort_values('Out_Length')
print(gdf)

#%%
import seaborn as sns
plt.subplot(2,1,1)
sns.regplot(x='Out_Length', y='LID_area', data=gdf, order=1)
plt.xlabel('Distance to Outfall B $(m)$')
plt.ylabel('LID area $(m^2)$')
plt.title('Relationship between LID area and distance to outfall')

plt.subplot(2,1,2)
sns.regplot(x='Out_Length', y='LID_ratio', data=gdf, order=2)
plt.xlabel('Distance to Outfall B $(m)$')
plt.ylabel('LID ratio $(\%)$')
plt.title('Relationship between LID ration and distance to outfall')

plt.tight_layout()
# plt.show()
plt.savefig('C:\\TV\\Results\\Distance_Area.jpg')