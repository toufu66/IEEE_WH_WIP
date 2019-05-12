#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 22:43:46 2019

@author: masahiro
"""

import open_csv_ as opcsv
import numpy as np
import random
import pickle as pkl


#fft_tap=128#model_vgg_3_400_velo_row_128
fft_tap=1024
#fft_tap=512
#fft_tap=256#model_vgg_3_400_velo_row_1
#fft_tap=768#model_vgg_3_400_velo_row_800

#sl_win=118
sl_win=64

for_num=1
with open("file_path.pkl", mode='rb') as f:
    DB_path=pkl.load(f)                

def batch_data(li):

    a=np.zeros([len(li),1,fft_tap])
    
    
#DFT321を使って加速度スペクトルを計算し、入力とする
    for i in range(len(li)):
        b=opcsv.open_csv(DB_path[li[i]])
        b=np.sqrt(np.sum(b*2,axis=1))
        #print(DB_path[li[i]])
        h=random.randint(0,b.shape[1]-fft_tap-(for_num-1)*sl_win)
        #for j in range(for_num):
        #c=np.fft.fft(b[:,h:h + fft_tap])
        #print(a[i].shape,c.shape)
        c=b[h:h + fft_tap]
        #if (max_c<np.max(c)):
        #    max_c=np.max(c)
        a[i]+=c            
        #a=np.sqrt(np.sum((opcsv.open_csv(ff[li[i]]))**2,axis=0))
        #print(a.shape)

        #h+=sl_win
        #a[i]=a[i]/for_num    
    #print(a.shape)
    #a=a/max_c
    a=np.transpose(a, [0,2,1])
    return a

ind=np.load("./ind.npy")    
def ind_to_label(li):
                                                                           
    #print(li,ind)
    lab=np.zeros([len(li),len(ind)-1],dtype="int16")
    for j in range(len(li)):    
        for i in range(1,len(ind)):
            #print("i,k",i-1,li[j],ind[i])
            if (ind[i] > li[j]) and (li[j]>= ind[i-1]):
                #lab[j,int(i-1)]=1
                #lab[j,int((((i-1)//45)*15+(i%15)))]=1
                lab[j,i-1]=1
                #print(lab[j])
                break
            
    return lab
