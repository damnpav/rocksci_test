# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 05:43:33 2019

@author: hcani
"""

from datetime import datetime
import pandas as pd
import numpy as np

folderRout = "C:/Users/hcani/Downloads/rocksci_test-master/rocksci_test-master/" #folder with files

currDf = pd.read_csv(folderRout+"currencies.csv")
exchDf = pd.read_csv(folderRout+"exchanges.csv")
pricesDf = pd.read_csv(folderRout+"prices.csv")
weightsDf = pd.read_csv(folderRout+"weights.csv")


def find_date(neededDate, colWithDates): #finding the closest date within column with dates
    flag = 0
    k = 0
    while flag == 0:
        if datetime.strptime(str(colWithDates.iloc[k, 0]),'%Y-%m-%d') < neededDate:
            k = k + 1
        else:
            flag = 1
    return(k)
    
nonUSD = np.where(currDf['currency'] != "USD")[0]
otherAssets = []
for i in range(len(nonUSD)):
    otherAssets.append(currDf['Unnamed: 0'][nonUSD[i]])

currencies = list(exchDf.columns[1:]) #list with Assets names
 
nonUSD = np.where(currDf['currency'] != "USD")[0] #find other currencies

otherAssets = [] #names of other assets
otherCurrencies = []
for i in range(len(nonUSD)):
   otherAssets.append(currDf['Unnamed: 0'][nonUSD[i]])
   otherCurrencies.append(currDf['currency'][nonUSD[i]])

nonUSD = np.where(currDf['currency'] != "USD")[0] #find other currencies
otherAssets = [] #names of other assets
otherCurrencies = [] #names of other currencies
for i in range(len(nonUSD)):
  otherAssets.append(currDf['Unnamed: 0'][nonUSD[i]])
  otherCurrencies.append(currDf['currency'][nonUSD[i]])
  dictAssets = dict.fromkeys(otherCurrencies) #lets fill dictionary where currency is a key


start_date = '2014-07-04'
end_date = '2014-07-09'
nonUSD = np.where(currDf['currency'] != "USD")[0] #find other currencies
otherAssets = [] #names of other assets
otherCurrencies = [] #names of other currencies
for i in range(len(nonUSD)):
    otherAssets.append(currDf['Unnamed: 0'][nonUSD[i]])
    otherCurrencies.append(currDf['currency'][nonUSD[i]])
dictAssets = dict.fromkeys(otherCurrencies) #lets fill dictionary where currency is a key
for key in dictAssets:
    keyValues = []
    for i in range(len(currDf['currency'])):
        if str(currDf['currency'][i]) == key:
            keyValues.append(currDf['Unnamed: 0'][i])
    dictAssets[key] = keyValues #dict with pairs Currency - Asset
myWeightsDf = weightsDf

myWeightsDf['BE0974268972 BB'] = myWeightsDf['BE0974268972 BB'] + myWeightsDf['DE0007164600 GR']
myWeightsDf = myWeightsDf.rename(columns= {'DE0007164600 GR': 'DE0007164600 GRdirty'})
otherAssets = otherAssets[:2]
for i in range(len(otherAssets)):
    myWeightsDf = myWeightsDf.rename(columns={otherAssets[i]: otherCurrencies[i]}) #replace assets names on currencies for calculating 
start_date = datetime.strptime(start_date, '%Y-%m-%d') 
end_date = datetime.strptime(end_date, '%Y-%m-%d') 
stIndex = find_date(start_date, exchDf)
enIndex = find_date(end_date, exchDf)
currencies = list(exchDf.columns[1:]) #list with currencies names
perf = []
for i in range(1, len(currencies)+1):
    subPerf = []        
    for j in range(stIndex, enIndex):
        subPerf.append((exchDf.iloc[j+1, i] - exchDf.iloc[j, i])/exchDf.iloc[j, i]) #perfomance for one currency
    perf.append(subPerf) #array with lists of perfomances 
dates = []
datetime_objects = []
for j in range(stIndex+1, enIndex+1):
    dates.append(exchDf.iloc[j, 0]) #list with dates in str format
    datetime_objects.append(datetime.strptime(str(exchDf.iloc[j, 0]), '%Y-%m-%d')) #list with dates in datetime format
dfPerf = pd.DataFrame(perf, index = currencies, columns = dates) #frame with perfomances for every asset
dfPerf = dfPerf.T

yieldsPerDay = []
#weights
for i in range(1, len(datetime_objects)): #perfomance for each day
    k = find_date(datetime_objects[i], myWeightsDf) # k is a number of day
    yields = []        
    for j in range(len(otherCurrencies)):
        #print(myWeightsDf.iloc[k][otherCurrencies[j]])
        yields.append(myWeightsDf.iloc[k][otherCurrencies[j]]*dfPerf.iloc[i][otherCurrencies[j]]) #weighted perfomance for each asset at one day
        #print(yields)
    yieldsPerDay.append(sum(yields)) #summarised perfomance for that day
    #print(yieldsPerDay)
cpDf = pd.DataFrame(yieldsPerDay, index = dates)
    
print(cpDf)


