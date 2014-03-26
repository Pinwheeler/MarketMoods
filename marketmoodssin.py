#marketmoodssin

#Market Psychology Analysis Tool
#With MySQL Database leverage
#
from __future__ import division
#setup
min_word_length = 2
min_word_frequency = 4
default_search_iterations = 4

#Import statements
import urllib, re, pymysql, ystockquote, nltk, urllib2, json
from nltk import FreqDist

#Connect to Database
db = pymysql.connect(host="localhost", user="root", passwd="", db="market_moods_db_backup")
cur = db.cursor()

#querey database for all company names
cur.execute("SELECT * FROM companies")
companies = cur.fetchall()
single_day_valence_dict = {}

def get_company_urls(c_name):
	"takes a company name and searches for the top urls"
	urlList = []
	#convert company name into a google-searchable company name
	c_name = re.sub(' ', '%20' , c_name)
	search_line = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + c_name
	response = urllib2.urlopen(search_line)
	search_results = json.loads(response.read())
	for result in search_results['responseData']['results']:
		urlList.append(result['visibleUrl'])
	return urlList

		


def get_relevant_words(c_name):
	"takes a list of URLs and strips out the relevant words"
	fulltext = ""
	for url in get_company_urls(c_name):
		#url = res.url.encode('utf8')
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
	return words

for row in companies :
	#get the stock change and price
	stock_name = row[0]
	stock_ticker = row[1]
	stock_change = ystockquote.get_change(row[1])
	stock_price = float(ystockquote.get_price(row[1]))


	continue_check = False

	try:
		float(stock_change[1:])
		continue_check = True
	except Exception, e:
		continue_check = False

	if continue_check:

		new_stock_change = 0
		# convert the stock change into a number
		if stock_change[0] == '+':
			new_stock_change = float(stock_change[1:])
		if stock_change[0] == '-':
			new_stock_change = -float(stock_change[1:])

		stock_change = new_stock_change

		overall_company_valence = 0
		company_word_count = 0

		words = get_relevant_words(stock_name)

		for word in words:
			word = word.lower()
			company_word_count = company_word_count + 1
			valence = 0
			count = 1
			execute_string = 'SELECT * FROM valences WHERE word = \"' + word + '\"'
			numrows = cur.execute(execute_string)
			wordrows = cur.fetchall()
			if numrows == 0:
				valence = abs(stock_change)
			else:
				valence = wordrows[0][1] + abs(stock_change)
				count = wordrows[0][2] + 1
			average_valence = valence / count
			overall_company_valence = overall_company_valence + average_valence

			#update global variances	
			args = (word,valence,count,average_valence)
			valence_string = "CALL updatevalence" + str(args)
			cur.execute(valence_string)

		#create single day valence list
		for word in words:
			word = word.lower()
			try:
				valenceArray = single_day_valence_dict[word]
			except Exception, e:
				single_day_valence_dict[word] = [0,0]
				valenceArray = single_day_valence_dict[word]
			
			valence = valenceArray[0]
			count = valenceArray[1]
			single_day_valence_dict[word] = [(valence + stock_change), (count +1)]

		#create prediction for tommorow
		try:
			overall_company_valence = overall_company_valence / company_word_count
		except Exception, e:
			overall_company_valence = 0.0	
		
		create_args = (stock_ticker, str(overall_company_valence), stock_name)
		create_string = str(create_args)
		cur.execute("CALL create_prediction" + create_string)

		#update movement table object with this information
		fetchargs = (stock_ticker,1,1,1)
		fetch_string = "CALL fetch_movement_today" + str(fetchargs)
		rows = cur.execute(fetch_string)
		movement = cur.fetchall()
		if movement:
			predicted_move = movement[0][2]
			difference = 0
			try:
				difference = stock_change - predicted_move
			except Exception, e:
				predicted_move = 1;
			if stock_change == 0:
				stock_change = 1
			percentage = 0
			try:
				percentage = min(stock_change,predicted_move)/max(stock_change,predicted_move)
			except Exception, e:
				percentage = 0
			movement_update_args = (stock_ticker,stock_change,difference,percentage,stock_name)
			
			update_string = "CALL evaluate_prediction" + str(movement_update_args)
			cur.execute(update_string)

	else:
		print stock_name + ": No Change in Stock Price"


for row in companies:
	#add the single day valence prediction to the database
	stock_name = row[0]
	stock_ticker = row[1]
	words = get_company_words(stock_name)

	overall_company_valence = 0

	for word in words:
		word = word.lower()
		try:
			valenceArray = single_day_valence_dict[word]
			averageWordValence = valenceArray[0]/valenceArray[1]
			overall_company_valence = overall_company_valence + averageWordValence
		except Exception, e:
			pass
	overall_company_valence = overall_company_valence / len(words)

	#upload to database
	uploadString = "CALL create_single_day_prediction" + str((stock_ticker,overall_company_valence))
	cur.execute(uploadString)


#commit and close connection
#disable this when testing the script
db.commit()

cur.close()
db.close()
print "MarketMoods run complete"
print('\a')

