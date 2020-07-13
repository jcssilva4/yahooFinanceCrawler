import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
def extractFromYahooFinance(assetCode): #basic info: name and sector
	#Download the Profile webpage. Store the 'Response' object in 'page'.
	assetCode = get_YFPROFILE_code(assetCode)  #get a valid assetCode
	current_url = 'https://finance.yahoo.com/quote/' + assetCode + '/profile?p=' + assetCode 
	page = requests.get(current_url)
	#analyse the page with BeautifulSoup4
	soup = BeautifulSoup(page.content,'html.parser')
	#get asset profile container
	profilecontainer = soup.findAll("div", {"class" : "qsp-2col-profile Mt(15px) Lh(1.7)"})
	container = profilecontainer[0]
	#get asset NAME
	assetNameContainer = container.findAll("h3", {"class" : "Fz(m) Mb(10px)" })
	assetName= assetNameContainer[0].getText()
	#get asset SECTOR
	assetSectorContainer = container.findAll("p",{"class" : "D(ib) Va(t)"})
	subcontainer = assetSectorContainer[0].findAll("strong")
	assetSector = subcontainer[0].getText()

	return [assetCode, assetName, assetSector]

def getSampleDates(thisURL):
	#create a new instance of  chrome
	driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
	#time.sleep(2)
	#go to the website of interest
	driver.get(thisURL)
	# Selenium script to scroll to the bottom, wait 3 seconds for the next batch of data to load, then continue scrolling.  It will continue to do this until the page stops loading new data.
	elm = driver.find_element_by_tag_name('html')
	for i in range(0,10): #change range if necessary
		elm.send_keys(Keys.END)
		print('press end')
		time.sleep(0.5)
	'''
	match = 0
	while match == 0:
		lastCount = lenOfPage
		time.sleep(3)
		lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		if lastCount==lenOfPage:
			match = 1
	'''
	# Now that the page is fully scrolled, grab the source code.
	source_data = driver.page_source

	# Throw your source into BeautifulSoup and start parsing!
	soup = BeautifulSoup(source_data, 'html5lib')
	dates = []
	#1- Download the webpage. Store the 'Response' object in 'page'.
	#page = requests.get("https://finance.yahoo.com/quote/PETR3/profile?p=PETR3")
	#page = requests.get(thisURL)
	#2- Response has a property named 'status_code' which indicates if the webpage was downloaded succesfully.
	#print("status code of the webpage: " , page.status_code, "!")
	#if page.status_code == 200: #a statuts code of 200 indicates that the page was downloaded.
		#analyse the page with BeautifulSoup4
		#soup = BeautifulSoup(page.content,'html5lib')
		#get table container
	priceTable = soup.findAll("div", {"class" : "Pb(10px) Ovx(a) W(100%)"})
	trash1 = priceTable[0].table
	for date in trash1.tbody:
		dates.append(date.span.getText())
	return dates
	
def  getHistoricalPrices(assetCode) :#get historical prices (Time period: Apr 01, 2015 - Jan 28, 2018) (OBS.: if tou want to change historical prices period of analysis you must change the URL base)
	#Download the Historical Prices webpage. Store the 'Response' object in 'page'.
	#1- Download the webpage. Store the 'Response' object in 'page'.
	#page = requests.get("https://finance.yahoo.com/quote/PETR3/profile?p=PETR3")
	prices = []
	current_url = "https://finance.yahoo.com/quote/" + assetCode + "/history?period1=1427511600&period2=1519873200&interval=1mo&filter=history&frequency=1mo"
	print('trying: ', current_url)
	page = requests.get(current_url)
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
					#print(element.getText())
					prices.append(element.getText())
	return prices


	

def get_YFPROFILE_code(assetCode): #this function returns a valid assetcode for Yahoo finance
	#1- Download the webpage. Store the 'Response' object in 'page'.
	#page = requests.get("https://finance.yahoo.com/quote/PETR3/profile?p=PETR3")
	#Some stock names are wrong. Fix them:
	if assetCode == 'SUZB5':
		assetCode = 'SUZB3' #http://www.guiainvest.com.br/publicacao/default.aspx?publicacao=704902
	if assetCode == 'TBLE3':
		assetCode = 'EGIE3' #https://exame.abril.com.br/mercados/tractebel-vira-engie-brasil-e-muda-codigo-de-acao-na-bolsa/ 
	print('extracting info for: ', assetCode)
	current_url = 'https://finance.yahoo.com/quote/' + assetCode + '.SA/profile?p=' + assetCode + '.SA'	 
	print('trying: ', current_url)
	page = requests.get(current_url)
	#2- Response has a property named 'status_code' which indicates if the webpage was downloaded succesfully.
	#print("status code of the webpage: " , page.status_code, "!")
	if page.status_code == 200: #a statuts code of 200 indicates that the page was downloaded.
		#analyse the page with BeautifulSoup4
		soup = BeautifulSoup(page.content,'html.parser')
		#get asset profile container
		profilecontainer = soup.findAll("div", {"class" : "qsp-2col-profile Mt(15px) Lh(1.7)"})
		if len(profilecontainer) == 0:
			#try another name (replace '.SA' for '' in the URL string)
			current_url = 'https://finance.yahoo.com/quote/' + assetCode + '/profile?p=' + assetCode 
		else:
			assetCode = assetCode + '.SA'
		return assetCode
	else:
		print("\nError: couldn't download the requested webpage")
		
