# -*- coding: utf-8 -*-
"""
Created on Thu Aug 1 04:58:57 2019

@author: Damir Pavlin
"""

import pandas as pd
import numpy as np
from datetime import datetime

folderRout = "C:/Users/hcani/Downloads/rocksci_test-master/rocksci_test-master/" #folder with files

currDf = pd.read_csv(folderRout+"currencies.csv")
exchDf = pd.read_csv(folderRout+"exchanges.csv")
pricesDf = pd.read_csv(folderRout+"prices.csv")
weightsDf = pd.read_csv(folderRout+"weights.csv")



class Portfolio:
    def cleanMySheet(giveMeUrSheet): #cleaning Sheet from Nans
        shapes = giveMeUrSheet.shape
        for i in range(shapes[0]): #cleaning data from Nans
            for j in range (1, shapes[1]):
                if pd.isnull(giveMeUrSheet.iloc[i, j]) == True:
                    if i == 0: #exception for the first elements
                        giveMeUrSheet.iloc[i, j] = giveMeUrSheet.iloc[:,j].mean()
                    else:
                        giveMeUrSheet.iloc[i, j] = giveMeUrSheet.iloc[i-1, j]
        return(giveMeUrSheet)
                    
    def find_date(neededDate, colWithDates): #finding the closest date within column with dates
        flag = 0
        k = 0
        while flag == 0:
            if datetime.strptime(str(colWithDates.iloc[k, 0]),'%Y-%m-%d') < neededDate:
                k = k + 1
            else:
                flag = 1
        return(k)
    
    def calculate_asset_performance(start_date, end_date): #start and end dates are string in format yyyy-mm-dd
        assets = list(pricesDf.columns) #list with Assets names
        start_date = datetime.strptime(start_date, '%Y-%m-%d') 
        end_date = datetime.strptime(end_date, '%Y-%m-%d') 
        stIndex = find_date(start_date, pricesDf)
        enIndex = find_date(end_date, pricesDf)
        perf = []
        for i in range(1, len(assets)):
            subPerf = []        
            for j in range(stIndex, enIndex):
                subPerf.append((pricesDf.iloc[j+1, i] - pricesDf.iloc[j, i])/pricesDf.iloc[j, i]) #perfomance for one asset
            perf.append(subPerf) #array with lists of perfomances
        dates = []
        datetime_objects = []
        for j in range(stIndex+1, enIndex+1):
            dates.append(pricesDf.iloc[j, 0]) #list with dates in str format
            datetime_objects.append(datetime.strptime(str(pricesDf.iloc[j, 0]), '%Y-%m-%d')) #list with dates in datetime format
        dfPerf = pd.DataFrame(perf, index = assets[1:], columns = dates) #frame with perfomances for every asset
        dfPerf = dfPerf.T
        yieldsPerDay = []
        #adding weigths
        for i in range(len(datetime_objects)): #perfomance for each day
            k = find_date(datetime_objects[i], weightsDf) # k is a number of day
            yields = []        
            for j in range(1, len(assets)):
                yields.append(weightsDf.iloc[k][assets[j]]*dfPerf.iloc[i][assets[j]]) #weighted perfomance for each asset at one day
            yieldsPerDay.append(sum(yields)) #summarised perfomance for that day
        wpDf = pd.DataFrame(yieldsPerDay, index = dates, columns = ["Asset perfomance"]) #frame with weighted perfomance
        return(wpDf)
    
    
#    def calculate_currency_performance(start_date, end_date): #TODO: resolve problem with currency duplicates
#        nonUSD = np.where(currDf['currency'] != "USD")[0] #find other currencies
#        otherAssets = [] #names of other assets
#        otherCurrencies = [] #names of other currencies
#        for i in range(len(nonUSD)):
#            otherAssets.append(currDf['Unnamed: 0'][nonUSD[i]])
#            otherCurrencies.append(currDf['currency'][nonUSD[i]])
#        dictAssets = dict.fromkeys(otherCurrencies) #lets fill dictionary where currency is a key
#        for key in dictAssets:
#            keyValues = []
#            for i in range(len(currDf['currency'])):
#                if str(currDf['currency'][i]) == key:
#                    keyValues.append(currDf['Unnamed: 0'][i])
#            dictAssets[key] = keyValues #dict with pairs Currency - Asset
#        myWeightsDf = weightsDf
#        for i in range(len(otherAssets)):
#            myWeightsDf = myWeightsDf.rename(columns={otherAssets[i]: otherCurrencies[i]}) #replace assets names on currencies for calculating 
#        start_date = datetime.strptime(start_date, '%Y-%m-%d') 
#        end_date = datetime.strptime(end_date, '%Y-%m-%d') 
#        stIndex = find_date(start_date, exchDf)
#        enIndex = find_date(end_date, exchDf)
#        currencies = list(exchDf.columns[1:]) #list with currencies names
#        perf = []
#        for i in range(1, len(currencies)+1):
#            subPerf = []        
#            for j in range(stIndex, enIndex):
#                subPerf.append((exchDf.iloc[j+1, i] - exchDf.iloc[j, i])/exchDf.iloc[j, i]) #perfomance for one currency
#            perf.append(subPerf) #array with lists of perfomances 
#        dates = []
#        datetime_objects = []
#        for j in range(stIndex, enIndex):
#            dates.append(exchDf.iloc[j, 0]) #list with dates in str format
#            datetime_objects.append(datetime.strptime(str(exchDf.iloc[j, 0]), '%Y-%m-%d')) #list with dates in datetime format
#        dfPerf = pd.DataFrame(perf, index = currencies, columns = dates) #frame with perfomances for every asset
#        dfPerf = dfPerf.T
#        yieldsPerDay = []
#        #weights
#        for i in range(len(datetime_objects)): #perfomance for each day
#            k = find_date(datetime_objects[i], myWeightsDf) # k is a number of day
#            yields = []        
#            for j in range(len(currencies)):
#                yields.append(myWeightsDf.iloc[k][currencies[j]]*dfPerf.iloc[i][currencies[j]]) #weighted perfomance for each asset at one day
#            yieldsPerDay.append(sum(yields)) #summarised perfomance for that day
#        cpDf = pd.DataFrame(yieldsPerDay, index = dates, columns = ["Currency perfomance"])
#        return(cpDf)
        
strategy = Portfolio()
Portfolio.calculate_asset_performance('2015-05-08', '2017-07-09')
#print(pricesDf.iloc[:,2])