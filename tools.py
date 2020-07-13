import os

def formatDate(dates):
	newDates = []
	for date in dates:
		newDate = [None]*3 #new format: YYYY-MM-DD
		formatedDate = date.split(',')
		newDate[0] = formatedDate[1].replace(' ', '') #get year 
		formatedDate2 = formatedDate[0].split(' ')
		newDate[2] = formatedDate2[1] #get day
		#get month
		if formatedDate2[0] == 'Jan':
			newDate[1] = '01'
		if formatedDate2[0] == 'Feb':
			newDate[1] = '02'
		if formatedDate2[0] == 'Mar':
			newDate[1] = '03'
		if formatedDate2[0] == 'Apr':
			newDate[1] = '04'
		if formatedDate2[0] == 'May':
			newDate[1] = '05'
		if formatedDate2[0] == 'Jun':
			newDate[1] = '06'
		if formatedDate2[0] == 'Jul':
			newDate[1] = '07'
		if formatedDate2[0] == 'Aug':
			newDate[1] = '08'
		if formatedDate2[0] == 'Sep':
			newDate[1] = '09'
		if formatedDate2[0] == 'Oct':
			newDate[1] = '10'
		if formatedDate2[0] == 'Nov':
			newDate[1] = '11'
		if formatedDate2[0] == 'Dec':
			newDate[1] = '12'
		newDate2 = '-'.join(newDate) #join everything
		newDates.append(newDate2)
	return newDates

def getQuadRanges(periods):
	script_dir = os.path.dirname(__file__)
	quadRanges = []
	for period in periods:
		relative_path = "composition/" + period + "range.txt"
		path = os.path.join(script_dir, relative_path)
		#get file object
		filehandle= open(path, "r")
		filelines = filehandle.readlines()
		rang = [filelines[0].replace('\n',''),filelines[1]]
		quadRanges.append(rang) 
		filehandle.close()	
	return quadRanges

def isContained(date,quadRange):
	lowerdate = quadRange[0].split('-')
	#print(lowerdate)
	upperdate = quadRange[1].split('-')
	#print(upperdate)
	currdate = date.split('-')
	#print(currdate)
	if(int(upperdate[0]) == int(lowerdate[0]) == int(currdate[0])):   #check if its the same year
		if(int(currdate[1]) == int(lowerdate[1])): #check month
			if(int(currdate[2]) >= int(lowerdate[2])): #check day
				return 1
			else:
				return 0
		elif (int(currdate[1]) == int(upperdate[1])): #check month
			if(int(currdate[2]) <= int(upperdate[2])): #check day
		 		return 1
			else:
				return 0
		elif(int(currdate[1]) > int(lowerdate[1]) and int(currdate[1]) < int(upperdate[1])): #check month only
			return 1
		else:
			return 0	
	elif(not(int(lowerdate[0]) == int(upperdate[0]))):
		if(int(lowerdate[0]) == int(currdate[0])): #check year
			if(int(currdate[1]) == int(lowerdate[1])): #check month
				if(int(currdate[2]) >= int(lowerdate[2])): #check day
					return 1
				else:
					return 0
			elif(int(currdate[1]) > int(lowerdate[1])): #check month
				return 1
			else: 
				return 0
		elif(int(upperdate[0]) == int(currdate[0])): #check year
			if (int(currdate[1]) == int(upperdate[1])): #check month
				if(int(currdate[2]) <= int(upperdate[2])): #check day
			 		return 1
				else:
					return 0
			elif(int(currdate[1]) < int(upperdate[1])): #check month
				return 1
			else:
				return 0
		else:
			return 0
	else:
		return 0