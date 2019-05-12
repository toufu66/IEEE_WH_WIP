#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 23:25:20 2019

@author: masahiro
"""

import os
import glob
import pickle as pkl
import numpy as np

if (os.path.exists("./li_train.npy")&os.path.exists("./li_test.npy")==False):
    dpath=os.getcwd()+"/../data_1k/"
    a0=[i+"/*" for i in glob.glob(dpath+"*.d")]
    cl_num=len(a0) #class number
    a1=[glob.glob(i) for i in a0]
    file_path=[]
    
    for i in range(cl_num):
        file_path.extend(a1[i])
    with open('file_path.pkl', mode='wb') as f:
        pkl.dump(file_path,f)
    indx_=[len(i) for i in a1]
    
    indx=[0]
    for i in range(0,5):
        indx.append(indx[-1]+indx_[i])
        
    np.save("./ind.npy",np.array(indx))
    
    li_train=[]#list index train
    li_test=[]#list index test
    for i in range(1,6):
        li_train=np.append(li_train,np.arange(indx[i-1],indx[i-1]+80))
        li_test=np.append(li_test,np.arange(indx[i]-16,indx[i]))
    li_train=np.array(li_train,dtype="int16")
    li_test=np.array(li_test,dtype="int16")
    np.save("li_train.npy",li_train)
    np.save("li_test.npy",li_test)
    #with open('train_path.pkl', mode='wb') as f:
    #    pkl.dump(train_path,f)
    #with open('test_path.pkl', mode='wb') as f:
    #    pkl.dump(test_path,f)
else:
    li_train=np.load("li_train.npy")
    li_test=np.load("li_test.npy")
        
    with open("file_path.pkl", mode='rb') as f:
        file_path=pkl.load(f)                
    #with open('test_path.pkl', mode='rb') as f:
    #    test_path=pkl.load(f)                