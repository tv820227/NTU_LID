# to calculate distance from subcatchment to outfall
#%%
import os
import pandas as pd
import numpy as np

os.chdir("..")

# import data from csv
conduit = pd.read_csv('conduit.csv', header=0)
subcatchment = pd.read_csv('subcatchment.csv', header=0)

# use left join to combine subcatchment and conduit
table = pd.merge(subcatchment, conduit, left_on='Outlet', right_on='From Node', how='outer')

# pick columns what I want and modify names of columns
table = table[['Name_x', 'From Node', 'To Node', 'Length']]
table.columns = ['Sub', 'From_Node', 'To_Node', 'Length']

# because outfall B is not in node, it will fill NaN after merging, we should fill B back
table[['From_Node', 'To_Node']] = table[['From_Node', 'To_Node']].fillna(value='B')
table['Length'] = table['Length'].fillna(value=0)

#%%
# to calculate the length from subcatchment to out fall B
node_dic = {f:[t,l] for f,t,l in zip(table['From_Node'], table['To_Node'], table['Length'])}

def length_to_out(node, dic=node_dic):
    '''Find the length from star node to outfall B'''
    #path = [node]
    length = 0
    while True:
        # record path and length
        #path.append(dic[node][0])
        length += dic[node][1]

        # find the next step
        node = dic[node][0]
        if node == 'B':
            break
    return length

table['Out_Length'] = table['From_Node'].agg(length_to_out)
table.to_csv('Out_Length.csv')
