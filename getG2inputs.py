#get Gaivoronski et al.' (2005) model inputs 
import numpy as np
import os
from asset import Asset
from tools import getQuadRanges
from tools import isContained

nPeriods = 6 #number of quads
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
#get prices 
sampleDateOk =  0 #used to get sample dates
sampleDates = []
for asset in assetList:
	relative_path = "IbovespaData/prices/" + asset.code + ".txt"
	path = os.path.join(script_dir, relative_path)
	#get file object
	filehandle= open(path, "r")
	filelines = filehandle.readlines()
	filehandle.close()
	for line in filelines:
		data = line.split('\t')
		asset.setDictPrices(data[0], data[1])
		if(not(sampleDateOk)):
			sampleDateOk = 1
			filelinesAux = filelines#used to get sample dates
			for dlines in filelinesAux:
				d = dlines.split('\t')
				sampleDates.append(d[0])
	'''
	if(asset.code == 'ABEV3'):
		print('\nPRICE (' + asset.name + '):' + str(asset.DictPrices['2015-10-06']) + '\n')
	'''''
#get Index prices
script_dir = os.path.dirname(__file__)
relative_path = "IbovespaData/prices/BVSPIDX.txt"
path = os.path.join(script_dir, relative_path)
#get file object
filehandle= open(path, "r")
filelines = filehandle.readlines()
filehandle.close()
IdxDictPrice = {}
datecounter = 0
for line in filelines:
	data = line.split('\t')
	IdxDictPrice[sampleDates[datecounter]] = data[1].replace('\n','')
	datecounter = datecounter + 1

#get rebalance dates
rebalanceDates = []
idxRDates = [] #maps rebalance dates in sampleDates
daycounter = 19 #rebalance interval
firstDayCounter = 0 #used to get 150 days sample 
sampleDays = 150 #number of days used to get inputs: expected return, covmat
idx = 0
for date in sampleDates:
	if(firstDayCounter <= sampleDays):
		firstDayCounter = firstDayCounter + 1
	else:
		if(daycounter == 19):
			rebalanceDates.append(date)
			idxRDates.append(idx)
			daycounter = 0
		else:
			daycounter = daycounter + 1
	idx  = idx + 1
print(rebalanceDates)
print(idxRDates)

#write IBOVESPA timeseries
quads = ['2018_1', '2017_3', '2017_2', '2017_1', '2016_3', '2016_2']
quadRanges = getQuadRanges(quads)
#print(quadRanges)
#print(idxRDates)
relative_path = "IbovespaData2/timeseries/ibovespaTimeSeries.txt"
path = os.path.join(script_dir, relative_path)
fileID = open(path, "w")
fileID.write("DATE\tNEGCODE\tNAME\tSECTOR\tWEIGHT\tFORWARDReturn\n")
notIncluded = []
ALLRMAT = [] #contains all sum(Ri)*sum(Rj) matrices
ALLRIDXVEC = [] #containe all Rt vectors
ALLRVEC = [] #sum(Rt)
ALLCMAT = [] #constraint coeficient Matrix
ALLASSETS = [] #contains all code vectors
rebalanceDates.reverse()
idxRDates.reverse()
print(rebalanceDates)
print(idxRDates)

idxrd = 1#index of idxRdates 
for date in rebalanceDates[1:]: #the last date will not be included (only used to get forward returns) 
	print(date)
	#get quad
	quadcounter = 0
	assetvec = []#used to write covmat
	observationsMatrix = [] #used to compute covmat
	for quad in quadRanges: #loop over nPeriods(period = four-month period)
		#print(quad)
		if(isContained(date,quad)):
			#print('contained')
			relative_path = "composition/" + quads[quadcounter] + ".txt"
			#print('open ' + relative_path)
			path = os.path.join(script_dir, relative_path)
			#get file object
			filehandle= open(path, "r")
			filelines = filehandle.readlines()
			filehandle.close()	
			#now you can find the assets contained here and read their weights and calculate their returns
			#get initial data (asset code and weights)
			nAssets = len(filelines) 
			code = [None]*nAssets
			benchWeight = [None]*nAssets
			for line in filelines:
				data_pt1 = line.split('\t')
				neg_code = data_pt1[0] #negotiation code
				benchWeight = (float(data_pt1[len(data_pt1)-1].replace('\n','')))/100 #transform from % to double dividing by 100
				currAsset = []
				for asset in assetList:
					if(asset.code == neg_code):
						currAsset = asset
						#get expected return
						idx = idxRDates[idxrd]
						samplePrices = [] #sample prices
						for r in range(0,sampleDays+1):
							#print(sampleDates[idx])
							price = currAsset.DictPrices[sampleDates[idx]].replace('\n','')
							if(not(price == '-')):
								samplePrices.append(float(price))
							idx = idx - 1
							'''
							if(asset.code == 'ABEV3' and r == 0):
								print('idx2 = ' + str(idx2) + '\tpriceSample = ' + str(samplePrices))
							'''
						sampleSize = len(samplePrices)#used as an insertion criteria
						p1 =  currAsset.DictPrices[rebalanceDates[idxrd-1]].replace('\n','') #future price
						if(len(samplePrices)<sampleDays+1): #do not include this asset (more data needed!)
							#print(asset.DictReturns)
							notIncluded.append((date + '\t' + neg_code + '\t' + currAsset.name + '\n'))
						elif(p1 == '-'): #future price  = 0
							p1 = 0
						else: #include this asset
							observationsMatrix.append(samplePrices)
							assetvec.append(neg_code)
							p0 =  currAsset.DictPrices[rebalanceDates[idxrd]].replace('\n','') #current price
							forwardR = (float(p1)-float(p0))/float(p0)
							fileID.write(date + '\t' + neg_code + '\t' + currAsset.name + '\t' + currAsset.sector + '\t' + str(benchWeight) + '\t' + str(forwardR) + '\n')
						break
		quadcounter = quadcounter + 1
	#print(idxRDates[idxrd])
	#print(sampleDates[idxRDates[idxrd]])
	#print(sampleDates[idxRDates[idxrd]+1])
	#get index Rt = sum in t((avgIdx_t/avgIdx_t-1 )- 1)for this date
	samplePrices = []
	idx =  idxRDates[idxrd]
	for r in range(0, sampleDays+1):
		price = IdxDictPrice[sampleDates[idx]]
		samplePrices.append(float(price))
		idx = idx - 1
	Rt = 0
	for r in range(0, sampleDays):
		Rt = Rt + (samplePrices[r]/samplePrices[r+1]) - 1
	idxrd = idxrd + 1
	#print(len(assetvec))
	observationsMatrix = np.array(observationsMatrix)
	#print(idxRDates[idxrd-1]) 
	#print(observationsMatrix.shape)
	#print(assetvec)
	#initialize cplex matrix and vec
	Cplexmat = []
	Cmat = []
	Cplexvec = []
	for i in range(0,len(assetvec)):
		matline = []
		for j in range(0,len(assetvec)):
			matline.append(0)
		Cplexmat.append(matline)
	#Cplexmat = np.array(Cplexmat)
	Cplexvec = matline#np.array(matline)
	for t in range(0, sampleDays):
		matline = []
		for i in range(0,len(assetvec) + 1): #include one more  col for the index!
			matline.append(0)
		Cmat.append(matline)
	#print(observationsMatrix.shape)
	#print(Cplexmat.shape)
	#get Cplex matrix
	matline = []
	for t in range(0,sampleDays):
		for i in range(0, len(assetvec)):
			ri = (observationsMatrix[i,t]/observationsMatrix[i,t+1])-1 #get return of i
			for j in range(0, len(assetvec)):
				rj = (observationsMatrix[j,t]/observationsMatrix[j,t+1])-1 #get return of j
				Cplexmat[i][j] = Cplexmat[i][j] + (ri*rj)
			Cmat[t][i] = ri
			Cplexvec[i] = Cplexvec[i] + ri
			#print(Cplexvec)
		Cmat[t][len(assetvec)] = (samplePrices[t]/samplePrices[t+1]) - 1 #get index return
	for i in range(0, len(assetvec)): #multiply Cplexvec by 2Rt and 1/T
		Cplexvec[i] = (2*Rt*Cplexvec[i])/sampleDays 
		for j in range(0, len(assetvec)):
			Cplexmat[i][j] = Cplexmat[i][j]/sampleDays #multiply Cplexmat by 1/T

	if( idxRDates[idxrd-1] == 151):
		print(observationsMatrix[0]) #abev3 mat
		print(Rt)
		print(Cplexmat[0][:])

	ALLRMAT.append(np.array(Cplexmat))
	ALLASSETS.append(assetvec)
	ALLRVEC.append(np.array(Cplexvec))
	ALLCMAT.append(np.array(Cmat))

fileID.close()
relative_path = "IbovespaData2/timeseries/notIncluded.txt"
path = os.path.join(script_dir, relative_path)
fileIDW= open(path,'w')
fileIDW.write("DATE\t DO NOT INCLUDE THIS ASSET\n")
for trash in notIncluded:
	fileIDW.write(trash)
fileIDW.close()

#get covmat
allIDX = 0 #use this to index ALLASSETS
for date in rebalanceDates[1:]:
	#print(date)
	relative_path = "IbovespaData2/rmat/rmat_" + date + ".txt"
	path = os.path.join(script_dir, relative_path)
	filemat = open(path,'w')
	asset = ALLASSETS[allIDX]
	#print(len(asset))
	mat = ALLRMAT[allIDX]
	#print(mat.shape)
	#print(mat)
	#write matcov's upper triangular 
	for i in range(0, len(asset)):
		for j in range(i, len(asset)):
			filemat.write(asset[i] + '\t' + asset[j] + '\t' + str(mat[i,j]) + '\n')
	filemat.close()
	allIDX = allIDX + 1

#write rvec
allIDX = 0 #use this to index ALLASSETS	
for date in rebalanceDates[1:]:
	relative_path = "IbovespaData2/rmat/rvec_" + date + ".txt"
	path = os.path.join(script_dir, relative_path)
	filemat = open(path,'w')
	asset = ALLASSETS[allIDX]
	#print(len(asset))
	mat = ALLRVEC[allIDX]
	#print(mat.shape)
	#print(mat)
	#write matcov's upper triangular 
	for i in range(0, len(asset)):
		filemat.write(asset[i] + '\t' + str(mat[i]) + '\n')
	filemat.close()
	allIDX = allIDX + 1

#write cmat
allIDX = 0 #use this to index ALLASSETS
for date in rebalanceDates[1:]:
	#print(date)
	relative_path = "IbovespaData2/rmat/cmat_" + date + ".txt"
	path = os.path.join(script_dir, relative_path)
	filemat = open(path,'w')
	asset = ALLASSETS[allIDX]
	#print(len(asset))
	mat = ALLCMAT[allIDX]
	#print(mat.shape)
	#print(mat)
	#write matcov's upper triangular 
	for t in range(0, sampleDays):
		for i in range(0, len(asset) +1):
			filemat.write(str(mat[t,i]) + '\t')
		filemat.write('\n')
	filemat.close()
	allIDX = allIDX + 1

relative_path = "IbovespaData2/rmat/samplePeriodSize.txt"
path = os.path.join(script_dir, relative_path)
filemat = open(path,'w')
filemat.write(str(sampleDays))
filemat.close()
