import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketmoods.settings')

import csv,ystockquote
import datetime
from justsearch import Searcher
from valence.models import Article, Company

API_KEY = 'dj0yJmk9cEpaUjdUWlBWZEZmJmQ9WVdrOVVFUTRRMEZXTkdVbWNHbzlNVGswTnpJM05UVTJNZy0tJnM9Y29uc3VtZXJzZWNyZXQmeD1kNg--'
API_SECRET = '265e6cbc321feb97b6e8b7a8fb006a1658687f29'

def upload_articles(company):
	search = Searcher(API_KEY,API_SECRET)
	try:
		results = search.news_search(company.name)['bossresponse']['news']['results']
	except:
		results = []
	if len(results) == 0:
		print "%s has no results" % company.name
	else:
		for entry in results:
			#print entry
			a = Article.objects.filter(title=entry['title'])
			if len(a) == 0:
				date = datetime.date.fromtimestamp(float(entry['date']))
				print "%s :: %s :: %s :: %s" % (str(date),company.name, entry['title'],str(entry['url']))
				article = Article(
					company=company,
					url=entry['url'],
					title=entry['title'],
					date=date,
					)
				article.save()

if __name__ == "__main__":
	for company in Company.objects.all():
		upload_articles(company)