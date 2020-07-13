''''
=== README ===

some observarions:
-we are using the 3rd prevision of the benchmark of jan-abr2017. That means some marginal deviations from
 the true weights might occur, but all asset names are ok! You can check this comparing  3prIBOVESPA set2017.xls
 and  2017_3.txt( the .txt was obtained in exame.com.br)

loop for begins here. Sugestion: 
globalData-> contains blocks of IbovespaData
year = 1
for t = 1:3*numyears
	 -colect data for quad_201(6 + (year-1))
	 -indicate which asset belongs to each period
	 if quad == 3
	 	year= year + 1
for IbovespaData in globalData
	get all individual assets of all periods and try to get a membership matrix, where each column is a period and each row is an asset. Each bij belongs to {0,1} , where 0 indicates that asset i is  not contained in period j
for j in 3*numyears
for asset in AllAssets
	get returns  Dec 30, 2014 - Fev 28, 2018
	get j return and store it in globalData_j
**finally, use the membership matrix to get covariance matrices
'''''

import requests
import os
from bs4 import BeautifulSoup
from getYahooData import extractFromYahooFinance 

#get current directory
script_dir = os.path.dirname(__file__)
nRebalances = 24
nPeriods = int(nRebalances/4)#number of benchmarks to be analysed= nMonths/nQuadperPeriod
IbovespaData = [None]*nPeriods
X = 2016 #begins in 2016
quad = 2 #begins in the second four-month period
p = 0 #period counter
print("num of periods to be analysed: ",nPeriods)
for t in range(0, nPeriods):
	relative_path = "composition/" + str(X) + "_" + str(quad) +".txt"
	path = os.path.join(script_dir, relative_path)
	#get file object
	filehandle= open(path, "r")
	filelines = filehandle.readlines()
	filehandle.close()
	#get initial data (asset code and weights)
	nAssets = len(filelines) 
	print( "The " + str(X)+ "." + str(quad) + " benchmark consists of "+ str(len(filelines)) + "assets ")
	code = [None]*nAssets
	benchWeight = [None]*nAssets
	i = 0 #aux index for code and bweight
	for  line in filelines:
		data = line.split('\t')
		#print(data[0], data[len(data)-1])
		code [i] = data[0]
		benchWeight[i] = (float(data[len(data)-1].replace('\n','')))/100 #transform from % to double dividing by 100
		i = i + 1	
	#append data
	#IbovespaData = IbovespaData.append(code)
	if quad == 3:
		quad = 1 #reset quad
		X = X + 1 #go to the next year
	else:
		quad = quad + 1
	IbovespaData[p] = [code, benchWeight]
	p = p + 1

#create asset objects
dataBlock = IbovespaData[0]
allAssets = dataBlock[0] #initialize allAssets variable
counter = 0
for dataBlock in IbovespaData: #get all assets which participated in the index during the analysis period (unique asset list)
	assetList = dataBlock[0]
	allAssets = set(assetList).union(allAssets) 	
offlineAssets = ['SUZB5', 'TBLE3', 'VALE5','CTIP3','RUMO3','SMLE3'] #these negotiation codes no longer exist at yahoo server 
onlineAssets = set(allAssets) - set(offlineAssets) #yahoo server contain these negotiation codes
IbovespaAssets = [None]*len(allAssets)
dataPart1 = [None]*len(allAssets) #base data set...use this to get returns, betas, covmatrix
assetCounter = 0 #aux index for dataPart1
for code in allAssets:
	periodInclusion = [None]*nPeriods
	situation = ''
	if code in onlineAssets:
		situation = 'on'
		rawdata = extractFromYahooFinance(code)
		yahooCode = rawdata[0]
		name = rawdata[1]
		if name == '':
			 name = 'insertName'
		sector = rawdata[2]
		if sector == '':
			 name = 'insertSector'
	if code in offlineAssets:
		situation = 'off'
		yahooCode = 'NULLCODE'
		name = 'insertName'
		sector = 'insertSector'
		print(code + " is offline")
	t = 0 #period counter...used in the next loop
	for dataBlock in IbovespaData: #get boolean list that indicates in which period 'code' participates
		assetList = dataBlock[0]
		if code in assetList:
			periodInclusion[t] = 1
		else:
			periodInclusion[t] = 0
		t = t + 1
	dataPart1[assetCounter] = [code, situation, yahooCode, name, sector, periodInclusion]
	assetCounter = assetCounter + 1
print(dataPart1)

#write dataPart1 in the disk
relative_path = "IbovespaData/dataPart1.txt"
path = os.path.join(script_dir, relative_path)
#get file object
filehandle= open(path, "w")
filehandle.write("CODE\tSITUATION\tYAHOOCODE\tNAME\tSECTOR\t")
for t in range(0,nPeriods):
	filehandle.write('memberP' + str(t+1) + "\t")
for line in dataPart1:
	filehandle.write("\n")
	counter  = 0 #element counter
	for element in line:
		print(counter)
		if counter  < len(line)-1:
			filehandle.write(str(element) + "\t")
		elif counter == len(line) - 1:  
			matrixLine = element
			print(matrixLine)
			for col in matrixLine:
				print(col)
				filehandle.write(str(col) + "\t")
		counter = counter + 1
filehandle.close()
