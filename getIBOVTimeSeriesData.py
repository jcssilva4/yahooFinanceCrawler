import os

'''
performance strategy: forget opening and closing files...read and connect all the COTAHIST files
'''

def getHistoricalPrices2(assetCode, dates):
	prices = []
	script_dir = os.path.dirname(__file__)
	filelines = []
	linesUsed = 0
	templines = 0
	for year in range (2015,2019):
		relative_path = "seriecotacoes/COTAHIST_A" + str(year) +".txt"
		path = os.path.join(script_dir, relative_path)
		#get file object
		filehandle= open(path, "r")
		filelines.extend(filehandle.readlines())
		if(year < 2018):
			filelines[len(filelines)-1] = filelines[len(filelines)-1]  + '\n'	
		filehandle.close()
		print(year)
	#line[2:10]-> date
	#line[12:24].replace(' ','')-> negotiation code
	#line[108:121]-> close price
	for d in dates:
		datediv = d.split('-')
		date = ''.join(datediv)
		templines = linesUsed
		price = []
		for line in filelines[linesUsed:len(filelines)-1]:
			if(line[2:10] == date):
				if(line[12:24].replace(' ','') == assetCode):
					price = str(float(line[108:121])) #we use float to transform '00000XX' into 'XX'
					linesUsed = templines
					break
				templines = templines + 1
		if(len(price) == 0): #tcouldn't find the specific assetCode at date
				prices.append('-')
		elif(len(price) > 0):
			if(len(price) < 3):
				prices.append(price)
			elif(len(price)==3):
				prices.append(str(float(price)/10))
			else:
				prices.append(str(float(price)/100))
		print(prices)
	return prices

#def getHistoricalPrices3(assetList, dates):


def adjustForCOTAHISTFile(rebalanceDates):
	dates = []
	script_dir = os.path.dirname(__file__)
	filelines = []
	linesUsed = 1
	templines = 1
	for year in range (2015,2019):
		relative_path = "seriecotacoes/COTAHIST_A" + str(year) +".txt"
		path = os.path.join(script_dir, relative_path)
		#get file object
		filehandle= open(path, "r")
		filelines.extend(filehandle.readlines())
		if(year < 2018):
			filelines[len(filelines)-1] = filelines[len(filelines)-1]  + '\n'	
		filehandle.close()
		print(year)
	#print(filelines[len(filelines)-300:len(filelines)-1] )
	for date in reversed(rebalanceDates):
		#get current directory
		datediv = date.split('-')
		datetemp = ''.join(datediv)
		dateNotFound = 1	
		templines = linesUsed
		print(datetemp)
		for line in filelines[linesUsed:len(filelines)-1]:
			print(line)
			#print(datetemp)
			if(line[2:10] == datetemp):
				dateNotFound = 0
				dates.append('-'.join(datediv))
				linesUsed = templines 
			if(not(dateNotFound) and line[2:10] == datetemp):
				print('ge')
				linesUsed = linesUsed + 1
			else:
				break
			templines = templines + 1
		while(dateNotFound):
			templines = linesUsed
			increment = 1 #you can only go forward in time
			if(datediv[2] == '31'):  #go forward one month, because you can't go backwards
				if(not(datediv[1]=='12') ): #if its not december
					tempdatediv1 = int(datediv[1]) + increment
					if(tempdatediv1 > 9):
						datediv[1] = str(tempdatediv1) 
					else:
						datediv[1] = '0' + str(tempdatediv1)
				else: 
					datediv[1] = '01'
					datediv[0] = str(int(datediv[0]) + 1)
					datediv[2] = '00'
			if(float(datediv[2]) >= 9 and float(datediv[2]) <=30):
				datediv[2] = str(int(datediv[2]) + increment)
			else:
				datediv[2] = '0' + str(int(datediv[2]) + increment)
			#print('not found')
			datetemp = ''.join(datediv)
			#print(datetemp)
			for line in filelines[linesUsed:len(filelines)-1]:
				if(line[2:10] == datetemp):
					dateNotFound = 0
					linesUsed = templines 
					dates.append('-'.join(datediv))
				if(not(dateNotFound) and line[2:10] == datetemp):
					linesUsed = linesUsed + 1
				else:
					break
				templines = templines + 1
		print(dates)
	return dates
		
def adjustForCOTAHISTFile2(initialDate, endDate):
	dates = []
	script_dir = os.path.dirname(__file__)
	filelines = []
	linesUsed = 1 #count number of lines that have been read
	templines = linesUsed  #used to support 'linesUsed'
	#read COTAHIST files
	for year in range (2015,2019):
		relative_path = "seriecotacoes/COTAHIST_A" + str(year) +".txt"
		path = os.path.join(script_dir, relative_path)
		#get file object
		filehandle= open(path, "r")
		filelines.extend(filehandle.readlines())
		if(year < 2018):
			filelines[len(filelines)-1] = filelines[len(filelines)-1]  + '\n'	
		filehandle.close()
		print(year)
	#print(filelines[len(filelines)-300:len(filelines)-1] )
	#get date
	datetemp = initialDate
	stop = 0
	print(datetemp)
	while(not(stop)):
		dateNotFound = 1
		templines = linesUsed
		for line in filelines[linesUsed:len(filelines)-1]:
			#print(datetemp)
			if(dateNotFound):
				if(line[2:6] == datetemp[0]): #check year
					if(line[6:8] == datetemp[1]): #check month
						if(line[8:10] == datetemp[2]):
							dateNotFound = 0
							dates.append('-'.join(datetemp))
							linesUsed = templines 
			elif(not(dateNotFound) and line[8:10] == datetemp[2]): #while in the same day...
				linesUsed = linesUsed + 1
			else:
				break
			templines = templines + 1
		#print('increment date ->' + str(datetemp))
		if(datetemp[2] == '31'):
			if(datetemp[1] == '12'): #then jump one year
				datetemp[0] = str(int(datetemp[0]) + 1)
				datetemp[1] = '01'
				datetemp[2] = '01'
			else: #jump one month
				if(int(datetemp[1]) >= 9):
					datetemp[1] = str(int(datetemp[1])+1)
					datetemp[2] = '01'
				else:
					datetemp[1] = '0' + str(int(datetemp[1])+1)
					datetemp[2] = '01'
		elif(int(datetemp[2]) >= 9):
			datetemp[2] =  str(int(datetemp[2])+1)
		else:
			datetemp[2] = '0' + str(int(datetemp[2])+1)
		if(datetemp[2] == endDate[2]) :
			if(datetemp[1] == endDate[1]):
				if(datetemp[0] == endDate[0]):
					stop = 1
		print(dates)
	return dates