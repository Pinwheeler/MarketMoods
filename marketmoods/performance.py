import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketmoods.settings')

import ystockquote
import datetime
from valence.models import Price, Company
today = datetime.date.today()
yesterday = today - datetime.timedelta(1)

def performance(date=yesterday,company={}):
	companies = Company.objects.filter(**company)
	start_date = date - datetime.timedelta(1)

	overall_change = 0.0
	overall_perc_change = 0.0
	average_change = 0.0
	average_perc_change = 0.0
	count = 0

	for _company in companies:
		start_price = Price.objects.filter(company=_company,date=start_date)
		if len(start_price) > 0: #convert from list of 1 item to 1 item
			start_price = float(start_price[0].price)
		else:
			print "no price data for %s" % str(start_date)
			continue
		end_price = Price.objects.filter(company=_company,date=date)
		if len(end_price) > 0: #convert from list of 1 item to 1 item
			end_price = float(end_price[0].price)
		else:
			print "no price data for %s" % str(date)
			continue
		overall_change += (end_price - start_price)
		overall_perc_change += ((end_price - start_price)/start_price)
		count += 1
	average_change = overall_change/count
	average_perc_change = overall_perc_change/count

	return {
	"performance_date":date,
	"change_sum": overall_change,
	"perc_sum": overall_perc_change,
	"count": count,
	"avg_change": average_change,
	"avg_perc": average_perc_change,
	}
