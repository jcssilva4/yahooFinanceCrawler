import requests
from bs4 import BeautifulSoup

#1- Download the webpage. Store the 'Response' object in 'page'.
page = requests.get("https://finance.yahoo.com/quote/PETR3.SA/history?period1=1427511600&period2=1519873200&interval=1mo&filter=history&frequency=1mo")
#2- Response has a property named 'status_code' which indicates if the webpage was downloaded succesfully.
#print("status code of the webpage: " , page.status_code, "!")
if page.status_code == 200: #a statuts code of 200 indicates that the page was downloaded.
	#analyse the page with BeautifulSoup4
	soup = BeautifulSoup(page.content,'html.parser')
	#get table container
	priceTable = soup.findAll("div", {"class" : "Pb(10px) Ovx(a) W(100%)"})
	trash1 = priceTable[0].table
	for block in trash1.tbody:
		#print(block)
		count = 0 #count elements
		for element in block: #get close price of the period
			count = count + 1
			if count == 5:
				print(element.getText())


	'''
	print(assetName)
	#get asset SECTOR
	assetSectorContainer = container.findAll("p",{"class" : "D(ib) Va(t)"})
	subcontainer = assetSectorContainer[0].findAll("strong")
	print(subcontainer[0].getText())
	'''
else:
	print("\nError: couldn't download the requested webpage")
