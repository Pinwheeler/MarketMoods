#Market Psychology Analysis Tool
#Author: Anthony Dreessen <anthonydreessen@gmail.com> pinwheeldesign.us
#

#setup
import BeautifulSoup
import urllib, re, pickle, sys
import nltk
from nltk import FreqDist
#from nltk import stopwords
from xgoogle.search import GoogleSearch, SearchError

word_count = {" " : 0}
fin = open("valence.dat", "r")
try: valence = pickle.load(fin)
except Exception, e:
	valence = dict()
fin.close()

frequency = 0

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")

#get a search term when opening up the module
search_name = raw_input("Input Seach Term: ")
search_depth = raw_input("Input Search Depth (20-200): ")
if search_depth > 200:
	search_depth = 200
if search_depth < 20:
	search_depth = 20
frequency = raw_input("Input mimimum frequency: ")

#perform google search
gs = GoogleSearch(search_name)
gs.results_per_page = search_depth
cum_valance_score = 0
results = gs.get_results()
fulltext = ""
for res in results:
	url = res.url.encode('utf8')
	print url
	html = urllib.urlopen(url).read()
	raw = nltk.clean_html(html)
	fulltext = fulltext + " " + raw

#Convert the raw text into an nltk Text object
tokens = nltk.wordpunct_tokenize(fulltext)
text = nltk.Text(tokens)

fdist = FreqDist(text)
#Get all words with length > 5 that are not on the stopword list
stopwords = nltk.corpus.stopwords.words('english')
words = sorted([w for w in set(text) if len(w) >= 5 and fdist[w] > int(frequency) and w.lower() not in stopwords])

for word in words:
	if word not in valence:
		input_string = "Input Valence of word " + word + " :"
		word_valence = raw_input(input_string)
		valence[word] = word_valence
		fout = open("valence.dat", "w")
		pickle.dump(valence, fout, protocol=0)
		fout.close()

for word in words:
	word_score_total = 0
	try: word_score_total = int(valence[word]) * relevant_fdist[word]
	except Exception, e:
		pass		
	cum_valance_score = cum_valance_score + word_score_total
print "Cumulative Valance: " + str(cum_valance_score)










