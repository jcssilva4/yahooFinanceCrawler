import os

price = []
#get current directory
assetCode = 'VIVR3'
date = '2015-05-04' #YYYY-MM-DD
datediv = date.split('-')
date = ''.join(datediv)
script_dir = os.path.dirname(__file__)
relative_path = "seriecotacoes/COTAHIST_A" + datediv[0] +".txt"
path = os.path.join(script_dir, relative_path)
#get file object
filehandle= open(path, "r")
filelines = filehandle.readlines()
filehandle.close()	
#line[2:10]-> date
#line[12:24].replace(' ','')-> negotiation code
#line[108:121].replace('0','')-> close price
for line in filelines:
	if(line[2:10] == date):
		if(line[12:24].replace(' ','') == assetCode):
			price = line[108:121].replace('0','')