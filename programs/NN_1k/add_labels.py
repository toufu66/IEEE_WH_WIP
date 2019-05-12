#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 15:11:43 2019

@author: masahiro
"""

import os
import glob
import pickle as pkl
import numpy as np

with open('material_label.pickle', mode='rb') as f:
    l=pkl.load(f)

data_dir="datas"
path=os.getcwd()+"/"+data_dir+"/add/"
a=[]
y=[]
d=[]
for i in range(len(l)):
    b=glob.glob(path+"*"+l[i][0]+"*/*")
    if len(b)!=0:
        a.extend(b)
        d.extend(b)
        y_=np.zeros([len(b),30])
        y_[:,l[i][1]]=1
        y.extend(y_)
        
y=np.array(y,dtype="int16")
np.save("add_y.npy",y)
with open('add_csv_path_list.pickle', mode='wb') as f:
    pkl.dump(d,f)
