import csv
import os
from getIBOVTimeSeriesData import adjustForCOTAHISTFile2

script_dir = os.path.dirname(__file__)
#get sample dates
relative_path = "IbovespaData/returns/sampledates.txt"
path = os.path.join(script_dir, relative_path)
filehandle= open(path, "r")
sampleDates = []
for date in filehandle:
	sampleDates.append(date.replace('\n', ''))
#read csv
''''
row indexes:
0 - date
1- open
2- high
3- low
4- close
'''''
relative_path = "IbovespaData/BVSP.csv"
path = os.path.join(script_dir, relative_path)
csvfile = open(path, 'rt') 
spamreader = csv.reader(csvfile)
ibovdates = []
counter = 0
ibovcounter = 0
idxPrices = []
for row in spamreader:
	#print(row[0])
	if(row[0] in sampleDates): #get sample date from ibov dates (intersection between sampleDates and BVSP dates)
		idxPrices.append(row[4])

#write BVSP prices
relative_path = "IbovespaData/prices/BVSPIDX.txt"
path = os.path.join(script_dir, relative_path)
filehandle= open(path, "w")
datecounter = 0
for price in idxPrices:
	filehandle.write(sampleDates[datecounter] + '\t' + price + '\n')
	datecounter = datecounter + 1