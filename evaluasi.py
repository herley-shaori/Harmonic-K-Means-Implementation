# -*- coding: utf-8 -*-
"""
Created on Wed May 22 14:38:38 2019

@author: Anwar
"""
import numpy as np
import pandas as pd
import math

imis = pd.read_excel('cobaImputmiss0.15klust8.xlsx')
osa = pd.read_excel('data OSA-AF cek.xlsx')
mis = pd.read_excel('cobabuatmiss0.15.xlsx')

kategorik=[1,5,6,7,8,9,10,11]
numerik=[0,2,3,4]

dfmis = mis.values
dfisi = imis.values
dfimis = imis.values
dfosa = osa.values

for i in numerik:
    for j in range (len(dfisi[:,i])):
        dfisi[j,i] = (dfimis[j,i] - dfosa[j,i])**2
        
for i in kategorik:
    for j in range(len(dfisi[:,i])):
        if dfimis[j,i] != dfosa[j,i]:
            dfisi[j,i] = 1
        else:
            dfisi[j,i] = 0

jmlh = [0,0,0,0]
for i in numerik:
    for j in range(len(dfisi[:,i])):
        if round(dfisi[j,i]) != 0:
            jmlh[numerik.index(i)] = jmlh[numerik.index(i)] + dfisi[j,i]
        else:
            jmlh[numerik.index(i)] = jmlh[numerik.index(i)] 
    
b = [0,0,0,0]
for i in numerik:
    for j in range(len(dfisi[:,i])):
        if round(dfisi[j,i]) != 0:
            b[numerik.index(i)] = b[numerik.index(i)] + 1
        else:
            b[numerik.index(i)] = b[numerik.index(i)]
            
mean_numerik = []
for i in range(len(jmlh)):
    try:
        mean_numerik.append(jmlh[i]/b[i])
    except ZeroDivisionError:
        mean_numerik.append(0)    

rmse = []
for i in range(len(mean_numerik)):
    rmse.append(math.sqrt(mean_numerik[i]))
    
rmse_semua = math.sqrt(sum(jmlh) / sum(b))

missing = [0,0,0,0,0,0,0,0]
for i in kategorik:
    for j in range(len(dfmis[:,i])):
        if str(dfmis[j,i].astype(float)) == str(np.nan):
            missing[kategorik.index(i)] = missing[kategorik.index(i)] + 1
        else:
            missing[kategorik.index(i)] = missing[kategorik.index(i)]
            
satu = [0,0,0,0,0,0,0,0]
for i in kategorik:
    for j in range(len(dfisi[:,i])):
        if dfisi[j,i] == 1:
            satu[kategorik.index(i)] = satu[kategorik.index(i)] + 1
        else:
            satu[kategorik.index(i)] = satu[kategorik.index(i)]
            
akurasi = []
for i in range(len(satu)):
    try:
        akurasi.append((missing[i]-satu[i])/missing[i])
    except ZeroDivisionError:
        akurasi.append(0)
        
akurasi_semua = (sum(missing) - sum(satu))/sum(missing)
        
dibutuhin=[akurasi,akurasi_semua,rmse,rmse_semua,missing,b]
with open('cobacobaEvaluasi0.15klust8.txt','w') as h:
    for i in dibutuhin:
        h.write(str(i)+"\n"+"\n")
