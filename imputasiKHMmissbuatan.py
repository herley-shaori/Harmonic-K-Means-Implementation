# -*- coding: utf-8 -*-
"""
Created on Wed May 22 11:12:44 2019

@author: Anwar
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 14:41:16 2019

@author: Anwar
"""

import pandas as pd
from math import factorial as fact
from itertools import combinations
from numpy import array,mean,nanmin,nanmax,isnan
import random

def alpha(i,klstr,jrkdk):
    sumasi=0
    for j in range(klstr):
        sumasi+=(1/jrkdk[i][j])**2
    return 1/sumasi**2
def qij(i,j,klstr,jrkdk):
    a=alpha(i,klstr,jrkdk)
    return a/(jrkdk[i][j])**4
def qj(j,klstr,jrkdk,lenobs):
    sumasi=0
    for i in range(lenobs):
        sumasi+=qij(i,j,klstr,jrkdk)
    return sumasi
def pij(i,j,klstr,jrkdk,lenobs):
    return qij(i,j,klstr,jrkdk)/qj(j,klstr,jrkdk,lenobs)
def rsubset(arr,r):
    return list(combinations(arr,r))

def chunk(xs,n):
    ys=list(xs)
    random.shuffle(ys)
    ylen=len(ys)
    size=int(ylen/n)
    chunks=[ys[size*i:size*(i+1)] for i in range(n)]
    edge=size*n
    leftover=ylen-edge
    for i in range(leftover):
        chunks[i%n].append(ys[edge+i])
    return chunks
    
df=pd.read_excel('cobabuatmiss0.15.xlsx')
dfori=pd.read_excel('cobabuatmiss0.15.xlsx')
df=df.drop([],axis=1)
namanya= "Usia Jenis_Kelamin IMT LP LL hipertensi merokok alkohol CHF Stroke PJK AF".split() 


dfsemua=df.values
kategorik=[1,5,6,7,8,9,10,11]
numerik=[0,2,3,4]
klust=8
T=100
#Normalisasi
for i in numerik:
    maxc=max(dfsemua[:,i])
    minc=min(dfsemua[:,i])
    maxminmin=maxc-minc
    for j in range(len(dfsemua[:,i])):
        dfsemua[j,i]-=minc
        dfsemua[j,i]/=maxminmin
totalkolom=kategorik.copy()
totalkolom.extend(numerik)
totalkolom.sort()
dfsemua1=pd.DataFrame(dfsemua,columns=totalkolom)
dffull=dfsemua1.dropna(axis=0)
simpen=dffull.copy()
dffull=dffull.values
for i in numerik:
    for j in range(len(dffull[:,i])):
        if dffull[j,i]<=1/3:
            dffull[j,i]=0
        elif dffull[j,i]<=2/3:
            dffull[j,i]=1
        else:
            dffull[j,i]=2
banyaklevelkat=dict()
for i in totalkolom:
    banyaklevelkat[i]=list(set(dffull[:,i]))
    banyaklevelkat[i]=[int(banyaklevelkat[i][k]) for k in range(len(banyaklevelkat[i]))]
pasangan=dict()
for i in totalkolom:
    pasangan[i]=[[] for k1 in totalkolom]
    a=fact(len(banyaklevelkat[i]))
    b=fact(len(banyaklevelkat[i])-2)*fact(2)
    for j in totalkolom:
        if i==j:continue
        for k1 in range(len(banyaklevelkat[j])):
            pasangan[i][j].append([])
            for k3 in range(int(a/b)):
                pasangan[i][j][k1].append([])
                for k2 in range(2):
                    pasangan[i][j][k1][k3].append(None)

for i in totalkolom:
    a=fact(len(banyaklevelkat[i]))
    b=fact(len(banyaklevelkat[i])-2)*fact(2)
    kommuncul=rsubset(banyaklevelkat[i],2)
    for j in totalkolom:
        if i==j:continue
        for k1 in range(len(banyaklevelkat[j])):
            for k4 in range(int(a/b)):
                for k2 in range(2):
                    sama=0
                    total=dffull[:,i].tolist().count(kommuncul[k4][k2])
                    for k3 in range(len(dffull[:,j])):
                        if dffull[k3,j]==banyaklevelkat[j][k1] and dffull[k3,i]==kommuncul[k4][k2]:sama+=1
                    pasangan[i][j][k1][k4][k2]=sama/total
                
hitungprobmax=dict()
for i in totalkolom:
    a=fact(len(banyaklevelkat[i]))
    b=fact(len(banyaklevelkat[i])-2)*fact(2)
    hitungprobmax[i]=[[] for k1 in totalkolom]
    for j in totalkolom:
        if i==j:continue
        for k1 in range(len(banyaklevelkat[j])):
            hitungprobmax[i][j].append([])
            for k4 in range(int(a/b)):
                hitungprobmax[i][j][k1].append([])
                hitungprobmax[i][j][k1][k4]=max(pasangan[i][j][k1][k4])
'''          
jarak1=dict()
for i in totalkolom:
    jarak1[i]=[[] for k1 in totalkolom]
    buatsum=[]
    for j in totalkolom:
        if i==j:continue
        for k1 in range(len(banyaklevelkat[j])):
            for k2 in range(len(banyaklevelkat[i])):
                try:
                    buatsum[k2].append(hitungprobmax[i][j][k1][k2])
                except IndexError:
                    buatsum.append([])
                    buatsum[k2].append(hitungprobmax[i][j][k1][k2])
        for k1 in range(len(banyaklevelkat[i])):
            jarak1[i][j][k1]=sum(buatsum[k1])-1
'''
jarak2=dict()
for i in totalkolom:
    jarak2[i]=[]
    a=fact(len(banyaklevelkat[i]))
    b=fact(len(banyaklevelkat[i])-2)*fact(2)
    buatsum=[]
    for j in totalkolom:
        if i==j:jarak2[i].append([0 for i in range(int(a/b))]);continue
        buatsum=array(hitungprobmax[i][j]).copy()
        buatsum=buatsum.T
        buatsum=buatsum.tolist()
        buatsum1=[]
        for k in range(int(a/b)):
            buatsum1.append(sum(buatsum[k])-1)
        jarak2[i].append(buatsum1)

jarak=dict()
for i in totalkolom:
    a=fact(len(banyaklevelkat[i]))
    b=fact(len(banyaklevelkat[i])-2)*fact(2)
    jarak[i]=[]
    buatmean=array(jarak2[i]).copy()
    buatmean=buatmean.T
    buatmean=buatmean.tolist()
    buatmean1=[]
    for k in range(int(a/b)):
        buatmean1.append(sum(buatmean[k])/(len(totalkolom)-1))
    jarak[i].append(buatmean1)
for i in jarak:
    jarak[i]=jarak[i][0]
bobot=dict()  
for i in totalkolom:
    if i in numerik:
        bobot[i]=mean(jarak[i])
    else:
        bobot[i]=0
            
initclust=chunk(simpen.values,klust)
updatecentroid=dict()
for i in range(klust):
    updatecentroid[i]=[[] for i in simpen]
    cursor=initclust[i]
    for j in totalkolom:
        if j in numerik:
            updatecentroid[i][j]=initclust[i][j].mean()
        else:
            arr=[]
            for k in banyaklevelkat[j]:
                a=[initclust[i][s][j] for s in range(len(initclust[i]))]
                arr.append(a.count(k)/len(a))
            updatecentroid[i][j]=arr
        
'''
jarak=dict()
for i in totalkolom:
    sumasi=0
    kolomkurang=totalkolom.copy()
    kolomkurang.remove(i)
    for j in kolomkurang:
        sumasi+=jarak1[i][j]
    jarak[i]=sumasi/(len(totalkolom)-1)
'''
ceksama=1
jarakdk=dict()
keanggotaan=dict()
for iterasi in range(T):
    #Ngitung jarak data ke centroid
    for j in range(dffull.shape[0]):
        cursor=simpen.iloc[j]
        jarakdk[j]=[None for i in range(klust)]
        for i in range(klust):
            sumasi=0
            for k in totalkolom:
                if k in numerik:
                    sumasi+=(bobot[k]*(cursor[k]-updatecentroid[i][k])**2)
                else:
                    sumdalam=0
                    for l in range(len(banyaklevelkat[k])):
                        if cursor[k]!=banyaklevelkat[k][l]:
                            a,b=min(cursor[k],banyaklevelkat[k][l]),max(cursor[k],banyaklevelkat[k][l])
                            kommuncul=rsubset(banyaklevelkat[k],2)
                            kali=jarak[k][kommuncul.index((a,b))]
                            kali*=updatecentroid[i][k][banyaklevelkat[k][l]]
                            sumdalam+=kali
                    sumasi+=(sumdalam)**2
            jarakdk[j][i]=sumasi
    #Keanggotaan
    for i in jarakdk:
        a=min(jarakdk[i])
        keanggotaan[i]=jarakdk[i].index(a)
    #update Centroid
    for j in range(klust):
        for s in totalkolom:
            if s in numerik:
                sumasi=0
                for i in range(dffull.shape[0]):
                    sumasi+=pij(i,j,klust,jarakdk,dffull.shape[0])*simpen.iloc[i][s]
                updatecentroid[j][s]=sumasi
            else:
                for k1 in range(len(banyaklevelkat[s])):
                    sumasi=0
                    for i in range(dffull.shape[0]):
                        cursor=simpen.iloc[i]
                        if cursor[s]==banyaklevelkat[s][k1]:
                            sumasi+=pij(i,j,klust,jarakdk,dffull.shape[0])
                updatecentroid[j][s][k1]=sumasi
    if ceksama==1:
        upd=keanggotaan.copy()
        ceksama=0
    else:
        if upd==keanggotaan:
            break
        else:
            upd=keanggotaan.copy()
listkeanggotaan=dict()
for i in range(klust):
    listkeanggotaan[i]=[]
for i in keanggotaan:
    listkeanggotaan[keanggotaan[i]].append(i)
        
centroid=updatecentroid.copy()    
dfmissingori=dfsemua1[dfsemua1.isnull().any(axis=1)]
dfmissing=dfsemua1[dfsemua1.isnull().any(axis=1)]
dfmissing=dfmissing.values
jrkmissing=dict()
for j in range(dfmissing.shape[0]):
    cursor=dfmissingori.iloc[j]
    jrkmissing[j]=[None for i in range(klust)]
    for i in range(klust):
        sumasi=0
        for k in totalkolom:
            if isnan(cursor[k]):
                continue
            if k in numerik:
                sumasi+=(bobot[k]*(cursor[k]-centroid[i][k])**2)
            else:
                sumdalam=0
                for l in range(len(banyaklevelkat[k])):
                    if cursor[k]!=banyaklevelkat[k][l]:
                        a,b=int(nanmin([cursor[k],banyaklevelkat[k][l]])),int(nanmax([cursor[k],banyaklevelkat[k][l]]))
                        kommuncul=rsubset(banyaklevelkat[k],2)
                        kali=jarak[k][kommuncul.index((a,b))]
                        kali*=centroid[i][k][banyaklevelkat[k][l]]
                        sumdalam+=kali
                sumasi+=(sumdalam)**2
        jrkmissing[j][i]=sumasi
#Keanggotaan
anggotamiss=dict()
for i in jrkmissing:
    a=min(jarakdk[i])
    anggotamiss[i]=jarakdk[i].index(a)

for i in anggotamiss:
    cursor=dfmissingori.iloc[i]
    for j in totalkolom:
        if isnan(cursor[j]):
            if j in numerik:
                dfmissing[i][j]=centroid[anggotamiss[i]][j]
            else:
                dfmissing[i][j]=centroid[anggotamiss[i]][j].index(max(centroid[anggotamiss[i]][j]))
df_new=pd.DataFrame(dfmissing,columns=totalkolom)
for i in range(dfmissing.shape[0]):
    dfmissingori.values[i]=df_new.values[i]
smth=[dfmissingori,simpen]
gabung=pd.concat(smth)
gabung=gabung.sort_index()
gabungarr=gabung.values
dfsemua=dfori.values
for i in numerik:
    maxc=max(dfsemua[:,i])
    minc=min(dfsemua[:,i])
    maxminmin=maxc-minc
    for j in range(len(gabungarr[:,i])):
        gabungarr[j,i]*=maxminmin
        gabungarr[j,i]+=minc
pd.DataFrame(gabungarr,columns=namanya).to_excel('cobaImputmiss0.15klust8.xlsx')
dibutuhin=[iterasi,listkeanggotaan,updatecentroid]
with open('cobaRangkuman0.15klust8.txt','w') as h:
    for i in dibutuhin:
        h.write(str(i)+"\n"+"\n")