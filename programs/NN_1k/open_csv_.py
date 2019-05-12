#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 08:51:39 2019

@author: masahiro
"""
import numpy as np
import pandas as pd
def open_csv(fpath):
    data= pd.read_csv(fpath,sep=",")
    npdata=np.array((data.values)[:,1:4])
    #npdata=npdata.reshape([7,-1])
    #print("aa")
    #長さがバラバラなので2400でカットして整形
    return npdata

#for j in[0,2,4]:

#tap=128
#c=4
#n=6
#fftz=[]
#a1_30=np.reshape(np.sqrt(np.sum(opcsv.open_csv(a1[c][n])**2,axis=1)),[1,-1])
#for i in range(0,((a1_30.shape[1])-tap)//1,1):
#    fftz.append(np.abs(np.fft.fft(a1_30[0,i:i+tap])[1:tap//2]))    
#fftz=np.array(fftz)
#plt.imshow(fftz.T,extent=[0,((a1_30.shape[1])-tap)/1000,512,0],aspect='auto')
#print(a1[c][n])
