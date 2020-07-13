''''
=== README ===

'''''


import requests
import os
from asset import Asset
from bs4 import BeautifulSoup
from getYahooData import getSampleDates
from getYahooData import getHistoricalPrices
from getIBOVTimeSeriesData import getHistoricalPrices2
from getIBOVTimeSeriesData import adjustForCOTAHISTFile2
from tools import formatDate

nRebalances = 24
nPeriods = int(nRebalances/4)#number of benchmarks to be analysed= nMonths/nQuadperPeriod
#get current directory
script_dir = os.path.dirname(__file__)
relative_path = "IbovespaData/raw_data_DB.txt"
path = os.path.join(script_dir, relative_path)
#get file object
filehandle= open(path, "r")
filelines = filehandle.readlines()
filehandle.close()	
#create asset objects
assetList = [None]*(len(filelines)-1) #initialize a list of assets
assetCounter = 0 #auxiliar idx for assetList
for line in filelines: #get asset name, sector, return
	data = line.split('\t')
	if(not(data[0] == 'CODE') ): #jump the header
		counter = 0 #element counter
		pMembership = [None]*nPeriods #boolean values that indicates if this asset is included in the benchmark at period p
		colcounter = 0 #membership matrix column counter
		for element in data[5:len(data)-1]: #get membership line
			pMembership[colcounter] = element
			colcounter = colcounter + 1
		assetList[assetCounter] = Asset(data[0], data[1], data[2], data[3], data[4], pMembership)
		assetCounter = assetCounter + 1
counter = 0

#get some rebalance dates in Yahoo finance
#sampleDates = getSampleDates('https://finance.yahoo.com/quote/BRFS3.SA/history?period1=1448938800&period2=1517367600&interval=1d&filter=history&frequency=1d')
#sampleDates = formatDate(sampleDates)
#adjust dates according to COTAHISTFile
sampleDates = adjustForCOTAHISTFile2(['2015','10','06'],['2018','02','06']) 
relative_path = "IbovespaData/returns/sampledates.txt"
path = os.path.join(script_dir, relative_path)
filehandle= open(path, "w")
for date in sampleDates:
	filehandle.write(date + '\n')
filehandle.close()

#get historical prices 
for asset in assetList:
	'''
	if (not(asset.yahooCode == 'NULLCODE')): #check if this code is online
		prices = getHistoricalPrices(asset.yahooCode)
		if (len(prices) > 0): #get returns from Yahoo Finance
			print(asset.code + ' historical prices  (' + rebalanceDates[len(rebalanceDates)-1] + ', '  + rebalanceDates[0] +  ') downloaded successfully')
			asset.setPrices(prices)
			print(asset.prices)
		else: #get returns from Ibovespa time series file
			print('failed to download ' + asset.code + ' from Yahoo Finance...trying to get prices from IBOVESPA timeseries file')
			prices = []
			for date in rebalanceDates:
				price = getHistoricalPrices2(asset.code, date)
				if(len(price) > 0):
					if(len(price) < 3):
						prices.append(price)
					elif(len(price)==3):
						prices.append(str(float(price)/10))
					else:
						prices.append(str(float(price)/100))
					print(prices)
			asset.setPrices(prices)
	else:
		print( "get " + asset.code + ' prices from IBOVESPA timeseries file')
		prices = []
		for date in rebalanceDates:
			price = getHistoricalPrices2(asset.code, date)
			if(len(price) > 0):
				if(len(price) < 3):
					prices.append(price)
				elif(len(price)==3):
					prices.append(str(float(price)/10))
				else:
					prices.append(str(float(price)/100))
				print(prices)
		asset.setPrices(prices)
	'''
	
	#HEREEE
	print( "get " + asset.code + ' prices from IBOVESPA timeseries file')	
	asset.setPrices(getHistoricalPrices2(asset.code, sampleDates))
#write prices in the disk
for asset in assetList:
	relative_path = "IbovespaData/prices/" + asset.code + ".txt"
	path = os.path.join(script_dir, relative_path)
	filehandle= open(path, "w")
	datecounter = 0
	print(len(asset.prices))
	if(len(asset.prices) < 37):
		print(asset.code)
	for price in asset.prices:
		filehandle.write(sampleDates[datecounter] + '\t' + str(price) + "\n")
		datecounter = datecounter + 1
	filehandle.close()
#HERE 
