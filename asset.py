class Asset:
	
	def __init__(self, c, s, yc, n, sec, pMembership):
		self.code = c
		self.yahooCode= yc
		self.name = n
		self.sector = sec
		self.belongsToPeriod = pMembership
		self.prices = []
		self.DictPrices = {} #lprices associated with some date
		self.returns = []
		self.DictReturns = {}

	def setPrices(self, prList):
		self.prices= prList
	def setDictPrices(self, date, price):
		self.DictPrices[date] = price
	def setReturns(self, rList):
		self.returns =rList
	def setDictReturns(self, date, retrn):
		self.DictReturns[date] = retrn
	#def getBeta():


