#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 21:25:40 2019

@author: masahiro
"""
from pylab import *
plt.plot(b)
plt.savefig("signal_row.png")
b=b.T
sl_win=8
fft_tap=512
rn=int((b.shape[1] -fft_tap)/sl_win)
spec=np.zeros([3,rn,int(fft_tap/2)-1])
for ch in range(3):
    
    for i in range(rn):
        spec[ch,i]=np.abs(np.fft.fft(b[ch,i*sl_win:i*sl_win+fft_tap]))[1:int(fft_tap/2)]
    
    

az=np.abs(np.fft.fft(b[:,0]))[1:250]
ax=np.fft.fft(b[500:1000,1])
ay=np.fft.fft(b[500:1000,2])


plt.imshow(spec[1].T)
plt.savefig("signal_x.png")

plt.imshow(spec[2].T)
plt.savefig("signal_y.png")

plt.imshow(spec[0].T)
plt.savefig("signal_z.png")

plt.plot(b.T)
