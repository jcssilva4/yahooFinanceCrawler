import os
from asset import Asset

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
#get prices and sampleDates
sampleDateOk =  0#used to get sample dates
sampleDates = []
for asset in assetList:
	script_dir = os.path.dirname(__file__)
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
			sampleDates.reverse()
#calculate returns
for asset in assetList:
	returns = []
	for datecounter in range(0, len(sampleDates) - 1):
		recentprice = asset.DictPrices[sampleDates[datecounter]]
		oldprice = asset.DictPrices[sampleDates[datecounter + 1]]
		if(not(recentprice == '-\n') and not(oldprice == '-\n')):
			r = (float(recentprice)-float(oldprice))/float(oldprice)
			returns.append(str(r))
		else:
			returns.append('-')
	asset.setReturns(returns)
#write returns
#write prices in the disk
for asset in assetList:
	relative_path = "IbovespaData/returns/" + asset.code + ".txt"
	path = os.path.join(script_dir, relative_path)
	filehandle= open(path, "w")
	print(len(asset.returns))
	for datecounter in range(0, len(sampleDates)-1):
		filehandle.write(sampleDates[datecounter] + '\t' + asset.returns[datecounter] + "\n")
		datecounter = datecounter + 1
	filehandle.close()

#get rebalance dates
rebalances = 0
rebalanceDates = []
while(rebalances < nRebalances) :#start from the most recent date
	rebalanceDates .append(sampleDates[rebalances])
	rebalances = rebalances + 1
#calculate forward returns