# This script should be run whenever a new MM database is created.
# the name of the base file is nyaindex.csv
# new file can be found at http://www.nyse.com/indexes/nyaindex.csv

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketmoods.settings')

import csv,ystockquote
from valence.models import Company
import urllib2

response = urllib2.urlopen('http://www.nyse.com/indexes/nyaindex.csv')

csvfile = response.read()
csvfile = ''.join(csvfile.split('\n')[1:])
dictreader = csv.DictReader(csvfile)
for entry in dictreader:
	price = float(ystockquote.get_price(ticker))
	ticker = entry['TICKER']
	if (price > 0):
		if Company.objects.filter(ticker=ticker):
			co = Company.objects.filter(ticker=ticker)
			co.price = price
			try:
				company.save()
			except Exception, e:
				print "Failed to Update: %s" %name
		else:	
			print "Adding %s :: %f" % (ticker,price)

			company = Company(
				name=entry['NAME'],
				ticker=entry['TICKER'],
				country=entry['COUNTRY'],
				icb=entry['ICB'],
				industry=entry['INDUS'],
				super_sector=entry['SUP SEC'],
				sub_sector=entry['SUB SEC'],
				price=price,
				)
			try:
				company.save()
			except Exception, e:
				print "Failed to Add: %s" %name
