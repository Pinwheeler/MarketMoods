import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketmoods.settings')

import csv,ystockquote
import datetime
from valence.models import Price, Company
today = datetime.date.today()
yesterday = today - datetime.timedelta(1)
startDate = today - datetime.timedelta(20)
backDate = today - datetime.timedelta(30)

def get_price_for_date(prices,date):
	price = 0
	new_date = None
	new_date_str = ""
	try:
		price = prices[str(date)]['Close']
	except Exception, e:
		new_date = date - datetime.timedelta(1)
		price = get_price_for_date(prices,new_date)
	if new_date != None:
		new_date_str = "->%s" % str(new_date)
	return price

def upload_historical_prices(company,backDate=backDate):
	ticker = company.ticker
	try:
		prices = ystockquote.get_historical_prices(ticker,str(backDate), str(yesterday))
		#print prices
	except Exception, e:
		#print "Failed to get historical prices for %s" % company.name
		return
	date = startDate
	while date < today:
		price = get_price_for_date(prices,date)
		p = Price.objects.filter(company = company, date = date)
		if len(p) == 0:
			p = Price(
				company=company,
				price=float(price),
				date=date,
				)
			print ("...Saving %s<%s>:%f" % (p.company.name, str(p.date), p.price))
			p.save()
		date = date + datetime.timedelta(1)

if __name__ == "__main__":
	company_count = len(Company.objects.all())
	count = 0
	for company in Company.objects.all():
		print "(%d/%d) Companies completed. Currently fetching %s..." % (count,company_count,company)
		upload_historical_prices(company)
		count += 1