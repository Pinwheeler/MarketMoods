import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketmoods.settings')

import csv,ystockquote
import datetime
import urllib2
import nltk
from nltk import FreqDist
from valence.models import Price, Company, Article, Valence
from pytz import timezone
from get_historical_prices import upload_historical_prices
today = datetime.date.today()
backDate = today - datetime.timedelta(20)
eastern = timezone('US/Eastern')
market_time = datetime.datetime.now(eastern)

## Settings Variables
min_word_length = 3
min_word_frequency = 3

def price_object_for_date(company,date):
	print ("Price for Company: %s Date: %s... " % (company.name,str(date)))
	if date < backDate:
		upload_historical_prices(company,backDate=date)
	price = Price.objects.filter(company=company,date=date)
	if price != None:
		print price
		if len(price) > 0:
			return price[0]
	new_date = date - datetime.timedelta(1)
	return price_object_for_date(company,new_date)

def find_valence_for_article(article):
	published_date = article.date
	affected_date = published_date + datetime.timedelta(1)
	company = article.company
	if market_time.hour < (12+5) and affected_date == today:
		return None
	pub_price = price_object_for_date(company,published_date).price
	aff_price = price_object_for_date(company,affected_date).price
	valence = aff_price - pub_price
	percent_valence = 100*((aff_price - pub_price)/pub_price)

	return(valence,percent_valence)


def score_article(article):
	valence_tup = find_valence_for_article(article)
	if valence_tup != None:
		print "Scoring Article: %s with valence (%f , %f)" % (article,valence_tup[0],valence_tup[1])
		company = article.company
		date = article.date
		valences = Valence.objects.filter(article=article)
		if len(valences) > 0: #If this article has already been scored
			print "...Article already scored"
			return
		try:
			html = urllib2.urlopen(article.url).read()
		except Exception, e:
			print ("Invalid Article URL, Deleting Article")
			article.delete()
			return
		raw = nltk.clean_html(html)
		raw = raw.replace('\n','')
		raw = raw.replace('\t','')
		raw = raw.lower()
		tokens = nltk.word_tokenize(raw)
		text = nltk.Text(tokens)
		fdist = FreqDist(text)
		#Get all words with length specified at top that are not on the stopword list
		stopwords = nltk.corpus.stopwords.words('english')
		words = sorted([w for w in set(text) if len(w) >= min_word_length and fdist[w] >= min_word_frequency and w.lower() not in stopwords])
		for word in words:
			valence = valence_tup[0]
			percent_valence = valence_tup[1]
			val = Valence(
				company=company,
				article=article,
				word=word,
				valence=valence,
				percent_valence=percent_valence,
				published_date=date,
				affected_date=(date + datetime.timedelta(1)),
				)
			try:
				if val.valence != 0: #0 represents noise
					val.save()
			except Exception, e:
				print ("Unarchivable word")


def for_date(date):
	if date == today:
		print "Can't score articles published today"
		return
	articles = Article.objects.filter(date=date)
	for article in articles:
		score_article(article)
		

def historical():
	for article in Article.objects.all():
		if article.date < today:
			score_article(article)

if __name__ == "__main__":
	historical()










