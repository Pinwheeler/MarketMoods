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
tomorrow = today + datetime.timedelta(1)
eastern = timezone('US/Eastern')
market_time = datetime.datetime.now(eastern)
min_word_length = 2
min_word_frequency = 2

def get_words_for_article(article):
	valences = Valence.objects.filter(article=article)
	if len(valences) > 0: #If this article has already been scored
		print ("......Article already scored")
		words = [valence.word for valence in valences]
		return words
	try:
		html = urllib2.urlopen(article.url).read()
		print "opening URL: %s" % str(article.url)
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
	return words

def predict(date=tomorrow,company={},article={},valence={}):
	"""all arguments are dicts containing filters pertaining to a model type"""
	companies = Company.objects.filter(**company)
	article['date'] = date - datetime.timedelta(2)

	change_sum = 0.0
	perc_sum = 0.0
	count = 0

	for _company in companies:
		print ("prediction for company: %s" %_company.name)
		article['company'] = _company
		articles = Article.objects.filter(**article)
		for _article in articles:
			print ("...Article:%s"%_article.title)
			words = get_words_for_article(_article)
			if words != None:
				for _word in words:
					valence['word']=_word
					valences = Valence.objects.filter(**valence)
					try:
						for _valence in valences:
							change_sum += float(_valence.valence)
							perc_sum += float(_valence.percent_valence)
							count += 1
					except Exception, e:
						print ("unsearchable word encountered, skipping")
	try:
		avg_change = (change_sum / count)
	except Exception, e:
		avg_change = 0
	try:
		avg_perc = (perc_sum / count)
	except Exception, e:
		avg_perc = 0
	return {
	"prediction_date": date,
	"change_sum": change_sum,
	"perc_sum": perc_sum,
	"count": count,
	"avg_change": avg_change,
	"avg_perc": avg_perc,
	}

if __name__ == "__main__":
	pred = predict()
	print pred
