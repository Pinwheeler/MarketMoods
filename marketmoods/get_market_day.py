import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketmoods.settings')

import csv,ystockquote
import datetime
from justsearch import Searcher
from valence.models import Company,Market_Day,Performance

today = datetime.date.today()
yesterday = today - datetime.timedelta(1)
tomorrow = today + datetime.timedelta(1)
API_KEY = 'dj0yJmk9cEpaUjdUWlBWZEZmJmQ9WVdrOVVFUTRRMEZXTkdVbWNHbzlNVGswTnpJM05UVTJNZy0tJnM9Y29uc3VtZXJzZWNyZXQmeD1kNg--'
API_SECRET = '265e6cbc321feb97b6e8b7a8fb006a1658687f29'

def get_company_results(c_name):
	"takes a company name and searches for the top news urls"
	resList = []
	#convert company name into a google-searchable company name
	search = Searcher(API_KEY,API_SECRET)
	result = search.news_search(c_name)

	for entry in result['bossresponse']['news']['results']:
		resList.append(result)
	return resList

def words_from_url(url):
	html = urllib.urlopen(url).read()
	raw = nltk.clean_html(html)
	raw = raw.replace('\n','')
	raw = raw.replace('\t','')
	tokens = nltk.word_tokenize(raw)
	text = nltk.Text(tokens)
	fdist = FreqDist(text)
	#Get all words with length > 5 that are not on the stopword list
	stopwords = nltk.corpus.stopwords.words('english')
	words = sorted([w for w in set(text) if len(w) >= min_word_length and fdist[w] >= min_word_frequency and w.lower() not in stopwords])
	return words

def word_logic(c_name,market_day):
	"""fetches articles for a company and attaches them to the market day
		also forms a prediction based on articles for today"""
	prediction_words = []
	for res in get_company_results(c_name):
		date = datetime.datetime.fromtimestamp(res['date'])
		url = res['url']
		words = words_from_url(url)
		if market_day.date < date < today: #then the article is from the marketday
			article = Article(market_day=market_day,url=url,title=res['title'])
			article.save()
			for word in words:
				wd = Word.objects.filter(word=word)
				if wd == None:
					wd = Word(word=word,articles.append(article))
				else:
					wd.articles.append(article)
				wd.save()
		if today < date < tomorrow:
			for word in words:
				wd = Word.objects.filter(word=word)
				if wd == None:
					pass
				else:
					prediction_words.append(wd)
		pred_change = 0
		pred_perc = 0
		for word in prediction_words:

				


for company in Company.objects.all():
	ticker = company.ticker
	curr_price = float(company.price)
	
	if curr_price > 0:
		price = float(ystockquote.get_price(ticker))

		if price > 0:
			market_day = Market_Day(
				company=company,
				date=yesterday,
				)
			market_day.save()

			performance = Performance(
				market_day=market_day,
				change_in_price=(price-curr_price),
				percent_change_in_price=(((price - curr_price)/curr_price)*100),
				)
			performance.save()

			company.price = curr_price
			company.save()
