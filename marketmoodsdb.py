#Market Psychology Analysis Tool
#With MySQL Database leverage
#
from __future__ import division
#setup
min_word_length = 5
min_word_frequency = 5

#Import statements
import urllib, re, pymysql, ystockquote, nltk
from nltk import FreqDist
from xgoogle.search import GoogleSearch, SearchError

#Connect to Database
db = pymysql.connect(host="localhost", user="root", passwd="", db="market_moods_db")
cur = db.cursor()

#querey database for all company names
cur.execute("SELECT * FROM companies")
companies = cur.fetchall()

for row in companies :
	#get the stock change and price
	stock_name = row[0]
	stock_change = ystockquote.get_change(row[1])
	stock_price = float(ystockquote.get_price(row[1]))


	continue_check = False

	try:
		float(stock_change[1:])
		continue_check = True
	except Exception, e:
		continue_check = False

	if continue_check:
		#create a new movements object with this information
		#
		#
		#

		new_stock_change = 0
		# convert the stock change into a number
		if stock_change[0] == '+':
			new_stock_change = float(stock_change[1:])
		if stock_change[0] == '-':
			new_stock_change = -float(stock_change[1:])

		stock_change = new_stock_change

		#perform google news search on company name
		gs = GoogleSearch(stock_name)
		gs.results_per_page = 50
		results = gs.get_results()
		fulltext = ""
		for res in results:
			url = res.url.encode('utf8')
			html = urllib.urlopen(url).read()
			raw = nltk.clean_html(html)
			fulltext = fulltext + " " + raw

		#Convert the raw text into an nltk Text object
		tokens = nltk.wordpunct_tokenize(fulltext)
		text = nltk.Text(tokens)

		fdist = FreqDist(text)
		#Get all words with length > 5 that are not on the stopword list
		stopwords = nltk.corpus.stopwords.words('english')
		words = sorted([w for w in set(text) if len(w) >= min_word_length and fdist[w] >= min_word_frequency and w.lower() not in stopwords])

		for word in words:
			word = word.lower()
			valence = 0
			count = 1
			execute_string = 'SELECT * FROM valences WHERE word = \"' + word + '\"'
			numrows = cur.execute(execute_string)
			wordrows = cur.fetchall()
			if numrows == 0:
				valence = stock_change
			else:
				valence = wordrows[0][1] + stock_change
				count = wordrows[0][2] + 1
			average_valence = valence / count	
			args = (word,valence,count,average_valence)
			cur.callproc("updatevalence",args)
	else:
		print stock_name + ": No Change in Stock Price"

#commit and close connection
db.commit()
print "Valences committed"

cur.close()
db.close()

