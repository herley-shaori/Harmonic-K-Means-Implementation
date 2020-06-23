 # -*- coding: utf-8 -*-
"""
Created on Tue May 21 15:35:48 2019

@author: Anwar
"""

import pandas as pd
import random
from sklearn.model_selection import train_test_split
import numpy as np
df=pd.read_excel('Data OSA-AF olah.xlsx')
df=df.drop(['Nama','BB','TB'],axis=1)
namanya= "Usia Jenis_Kelamin IMT LP LL hipertensi merokok alkohol CHF Stroke PJK AF".split() 
x_train, x_test=train_test_split(df,test_size=0.15)
testidx=x_test.index.tolist()
x_train1=x_train.values
x_test1=x_test.values
x_test_miss=x_test1.astype(float)
for x in range(len(x_test1)):
    hilang=random.choices([2,3,4,5,6])
    posisi=random.sample([0,1,2,3,4,5,6,7,8,9,10,11],hilang[0])
    for y in range(len(posisi)):
        x_test_miss[x][posisi[y]]=np.nan
gabung=df.copy().values
for i,t in enumerate(testidx):
    gabung[t]=x_test_miss[i]
gabung=pd.DataFrame(gabung)
gabungarr=gabung.values
dfsemua=df.values
pd.DataFrame(gabungarr,columns=namanya).to_excel('cobabuatmiss0.15.xlsx')        
