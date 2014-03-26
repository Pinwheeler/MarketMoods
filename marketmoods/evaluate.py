import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketmoods.settings')

import datetime
from valence.models import Price, Company
today = datetime.date.today()
yesterday = today - datetime.timedelta(1)
from predict import predict
from performance import performance

def evaluate(date=yesterday,company={}):
	companies = Company.objects.filter(**company)
	c_list = []
	for _company in companies:
		c_dict = {"ticker":_company.ticker,}
		pred = predict(date=date,company=c_dict)
		perf = performance(date=date,company=c_dict)
		try:
			accu = 100*abs((perf['avg_change'] - pred['avg_change'])/perf['avg_change'])
		except Exception, e:
			accu = None
		try:
			p_accu = 100*abs((perf['avg_perc'] - pred['avg_perc'])/perf['avg_perc'])
		except Exception, e:
			p_accu = None
		if accu != None:
			c_list.append({"accu":accu,"p_accu":p_accu,"pred":pred,"perf":perf})
	return c_list

