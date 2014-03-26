# This script should be run whenever a new MM database is created.
# the name of the base file is nyaindex.csv
# new file can be found at http://www.nyse.com/indexes/nyaindex.csv

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketmoods.settings')

import csv,ystockquote
from valence.models import Company

with open('nyaindex.csv') as csvfile:
    dictreader = csv.DictReader(csvfile)
    for entry in dictreader:
        ticker = entry['TICKER']
        c = Company.objects.filter(ticker=ticker)
        if c is not None:
            price = float(ystockquote.get_price(ticker))

            if price != 0:
                print "%s :: %f" % (ticker,price)

                company = Company(
                    name=entry['NAME'],
                    ticker=entry['TICKER'],
                    country=entry['COUNTRY'],
                    icb=entry['ICB'],
                    industry=entry['INDUS'],
                    super_sector=entry['SUP SEC'],
                    sub_sector=entry['SUB SEC'],
                    )
                try:
                    company.save()
                except Exception, e:
                    pass