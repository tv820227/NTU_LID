#%%
# import modules
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# change working directory
# path = "C:\\TV\\Results\\OptimalResult\\Result"
path = "C:\\Chung-Yuan\\Publish\\Result\\OptimalResult\\Billion\\Picked"
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
# len_file_path = "C:\\TV\\Results\\Out_Length.csv"
len_file_path = 'C:\\Chung-Yuan\\Publish\\Result\\Out_Length.csv'
length = pd.read_csv(len_file_path, header=0)
length = length[['Sub', 'Out_Length', 'Area']]

# concate all dataframe through rows and merge Length by 'Sub'
alldf = pd.concat(df_list, axis='rows', ignore_index=True)
alldf = pd.merge(alldf, length, on='Sub')

#%%
alldf['Sub'] = alldf['Sub'].astype('category')
alldf['LID_area'] = alldf['Bio_Area'] + alldf['Pav_Area']
alldf['LID_ratio'] = alldf['LID_area']/alldf['Area']*100
gdf = alldf.groupby('Sub').median()
gdf = gdf.sort_values('Out_Length')
print(gdf)


#%%
# calculat correlation coefficient between distance to origin and LID ratio
# shift origin and pick max/min one
l = list(gdf['Out_Length'])
ratio = np.array(gdf['LID_ratio'])
corr = [np.corrcoef(ratio, abs(np.array(l)-i))[0,1] for i in l]
min_x, min_y = l[corr.index(min(corr))], min(corr)

# plot datas
fig1 = plt.figure(1)
plt.scatter(min_x, min_y, marker='o', s=40, c='red')
plt.plot(l,corr, marker='.')
plt.text(min_x-50, min_y-0.05, s="min r="+str(round(min_y,2)))

# customer setting
plt.title('Correlation coeffcient between LID ratio\n and distance under different origin')
plt.xlabel('Distance between origin and B $(m)$')
plt.ylabel('Correlation coeffcient')
plt.axis([-20,620,-0.6,0.6])
plt.savefig('C:\\Chung-Yuan\\Publish\\Result\\New\\Hydrology Analysis\\Distance_correlation.jpg')
# plt.show()

#%%
import seaborn as sns
# gdf['Shift_L'] = np.array(l)-min_x

fig2 = plt.figure(2)
plt.subplot(2,1,1)
sns.regplot(x='Out_Length', y='LID_area', data=gdf, order=1)
plt.xlabel('Distance to Outfall B $(m)$')
plt.ylabel('LID area $(m^2)$')
plt.title('Relationship between LID area and distance to outfall')

plt.subplot(2,1,2)
sns.regplot(x='Out_Length', y='LID_ratio', data=gdf, order=2)
plt.xlabel('Distance to Outfall B $(m)$')
plt.ylabel('LID ratio $(\%)$')
plt.title('Relationship between LID ratio and distance to outfall')

plt.tight_layout()
# plt.show()
# plt.savefig('C:\\TV\\Results\\Distance_Area.jpg')
plt.savefig('C:\\Chung-Yuan\\Publish\\Result\\New\\Hydrology Analysis\\Distance_Area.jpg')