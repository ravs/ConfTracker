import re
import temporal_tagger_override
from datetime import datetime, date, time
try:
    from mx.DateTime import *
except ImportError:
    print """
Requires eGenix.com mx Base Distribution
http://www.egenix.com/products/python/mxBase/"""

word_list = []
f2 = open('pos_and_temporal_tagged_tweets.txt','w+')
f4 = open('ner_tagged_tweet.txt','w+')
p1 = open('id_tweets.txt','w+')

CONFcorpus = ""
HTTECHcorpus = ""
HTCONFcorpus = ""
USRCONFcorpus = ""
CONFACROcorpus = ""
POSITIVEcorpus = ""
NEGATIVEcorpus = ""


def generate_id_tweets():
	f1 = open('raw_input_tweets.txt','r+')
	for id,tweet in enumerate(f1):
		if len(tweet) > 0 and tweet != '' and tweet != "\n":
			tweet = "ID:"+str(id)+" " + tweet
			p1.write(tweet)

def split_words_in_tweets():
	# f1 = open('conf_training_set.txt','r+')
	# f1 = open('input.txt','r+')
	tagged_tweet_list = []
	f1 = open('tem_unlabelled_201_599.txt','r+')
	for id,tweet in enumerate(f1):
		id = id + 201
		if len(tweet) > 0 and tweet != '':
			tagged_tweet = process_tweet(tweet)
			temporal_tagged_tweet,temporal_value = temporal_tagger_override.tag(tweet)
			if len(temporal_value) != 0:
				try:
					# print temporal_tagged_tweet
					temporal_tweet_value = temporal_tagger_override.ground(temporal_tagged_tweet,now())
					tagged_tweet = tagged_tweet + " " + str(temporal_tweet_value) + "/TEMPORAL"
				except Exception as e:
					# print "Cannot convert to ISO time" + str(e)
					tagged_tweet = tagged_tweet + " " + ",".join(temporal_value) + "/TEMPORAL"
			else:
				tagged_tweet = tagged_tweet + " " + "NO" + "/TEMPORAL"
			tagged_tweet = "ID:"+str(id)+" " + tagged_tweet
			f2.write(tagged_tweet)
			f2.write("\n")
			tagged_tweet_list.append(tagged_tweet)
	return ",".join(tagged_tweet_list)

def split_words_in_tweets_i(tweet,id):
	if len(tweet) > 0 and tweet != '':
		tagged_tweet = process_tweet(tweet)
		temporal_tagged_tweet,temporal_value = temporal_tagger_override.tag(tweet)
		if len(temporal_value) != 0:
			try:
				# print temporal_tagged_tweet
				temporal_tweet_value = temporal_tagger_override.ground(temporal_tagged_tweet,now())
				tagged_tweet = tagged_tweet + " " + str(temporal_tweet_value) + "/TEMPORAL"
			except Exception as e:
				# print "Cannot convert to ISO time" + str(e)
				tagged_tweet = tagged_tweet + " " + ",".join(temporal_value) + "/TEMPORAL"
		else:
			tagged_tweet = tagged_tweet + " " + "NO" + "/TEMPORAL"
		tagged_tweet = "ID:"+str(id)+" " + tagged_tweet
	return tagged_tweet	

def load_corpus():
	global CONFcorpus, HTTECHcorpus, HTCONFcorpus, USRCONFcorpus, CONFACROcorpus
	corpus_list = []
	corpus_file_list = ["Reference_corpus.txt","HTTECH_corpus.txt", \
					"HTCONF_corpus.txt","USRCONF_corpus.txt", \
					"CONFACRO_corpus.txt","POSITIVE.txt","NEGATIVE.txt"]
	for i,corpus in enumerate(corpus_file_list):
		f3 = open(corpus,'r+')
		temp_pattern = []
		for word in f3:
			temp_pattern.append(word.rstrip("\n"))
		if i == 0:
			CONFcorpus = "|".join(temp_pattern)
		if i == 1:
			HTTECHcorpus = "|".join(temp_pattern)
		if i == 2:
			HTCONFcorpus = "|".join(temp_pattern)
		if i == 3:
			USRCONFcorpus = "|".join(temp_pattern)
		if i == 4:
			CONFACROcorpus = "|".join(temp_pattern)
		if i == 5:
			POSITIVEcorpus = "|".join(temp_pattern)
		if i == 6:
			NEGATIVEcorpus = "|".join(temp_pattern)
		f3.close()


def process_tweet(tweet):
	global corpus,POSITIVEcorpus,NEGATIVEcorpus
	tag_val1 = "NNCONF"
	tag_val0 = "O"
	tag_val3 = "USR"
	tag_val2 = "HANDLE"
	tag_val4 = "USRCONF"
	tag_val6 = "HTTECH"
	tag_val7 = "HTCONF"
	tag_val8 = "CONFACRO"
	tag_val10 = "URL"
	tag_val11 = "VBCONF"
	tag_val12 = "POSITIVE"
	tag_val13 = "NEGATIVE"
	pattern1 = '(' + CONFcorpus + ')'
	pattern2 = '@[A-Z]'
	pattern3 = '#[A-Z]'
	pattern4 = '^@' + '([A-Z]*)' + '(' + CONFcorpus + ')+' + '[A-Z]*'
	pattern6 = '(' + HTTECHcorpus + ')'
	pattern7 = '(' + HTCONFcorpus + ')'
	pattern8 = '(' + USRCONFcorpus + ')'
	pattern10 = 'http?:'
	VERBcorpus = open('VERB','r+').read()
	CONFACROcorpus = open('CONFACRO_corpus.txt','r+').read()
	POSITIVEcorpus = open('POSITIVE.txt','r+').read()
	NEGATIVEcorpus = open('NEGATIVE.txt','r+').read()
	# f4.write(" ")
	# f4.write("\n")
	tweet_words = []
	tweet_words = tweet.split()
	tweet_tagged = '' 
	for word in tweet_words:
		word = word.strip(r'[:;,_-]')
		word_lcase = word.lower()
		
		if re.search(pattern1,word,re.IGNORECASE) and word.find("@") == -1 and word.find("#") == -1:
			f4.write(str(word)+"/"+tag_val1)
			word = word+"/"+tag_val1
		elif re.search(pattern8,word,re.IGNORECASE):
			f4.write(str(word)+"/"+tag_val4)
			word = word+"/"+tag_val4
		# elif re.search(pattern2,word,re.IGNORECASE):
		# 	f4.write(str(word)+"/"+tag_val2)
		# 	word = word+"/"+tag_val2
		elif re.search(pattern7,word,re.IGNORECASE):
			f4.write(str(word)+"/"+tag_val7)
			word = word+"/"+tag_val7
		elif re.search(pattern3,word,re.IGNORECASE):
			f4.write(str(word)+"/"+tag_val3)
			word = word+"/"+tag_val3
		# elif re.search(pattern6,word,re.IGNORECASE):
		# 	f4.write(str(word)+"/"+tag_val6)
		# 	word = word+"/"+tag_val6	
		elif word in CONFACROcorpus:
			f4.write(str(word)+"/"+tag_val8)
			word = word+"/"+tag_val8
		elif re.search(pattern10,word,re.IGNORECASE):
			f4.write(str(word)+"/"+tag_val10)
			word = word+"/"+tag_val10
		elif word in POSITIVEcorpus:
			f4.write(str(word)+"/"+tag_val12)
			word = word+"/"+tag_val12
		elif word in NEGATIVEcorpus:
			f4.write(str(word)+"/"+tag_val13)
			word = word+"/"+tag_val13		
		elif word in VERBcorpus:
			f4.write(str(word)+"/"+tag_val11)
			word = word+"/"+tag_val11
		# else:
		# 	if word is not "":
		# 		# f4.write(str(word)+"/"+tag_val0)
		# 		word = word+"/"+tag_val0
		f4.write(" ")
		tweet_tagged = tweet_tagged + word + " "
	f4.write("\n")
	return tweet_tagged


load_corpus()
generate_id_tweets()
split_words_in_tweets()

