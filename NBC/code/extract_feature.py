#!/usr/bin/env python

'''
Python script to extract features from annotated tweet corpus
'''

import copy
import json

# List of tweets with corresponding feature vector
# tweet_feature_list = 
#[ "tweet_id": {
#				"feature_vector": { 
#									"NNCONF" : {"tokens": [], "no_of_tok": int},
#						  			"VBCONF" : {"tokens": [], "no_of_tok": int},
#						  		  	"USRCONF" : {"tokens": [], "no_of_tok": int},
#								  	"HTCONF" : {"tokens": [], "no_of_tok": int},
#				  				  	"INCONF" : {"tokens": [], "no_of_tok": int},
#				  				  	"TEMPORAL" : {"tokens": [], "no_of_tok": int},
#				  				  	"URL" : {"tokens": [], "no_of_tok": int}
#								},
#				"label": 0 or 1
#]
tweet_feature_list_train = []
tweet_feature_list_test = []
# Include POS tags in the list as per feature vector
# feature_vector_names = ["NNCONF","VBCONF","USRCONF","JJCONF","CONFACRO","HTCONF","INCONF","TEMPORAL","URL"]
feature_vector_names = ["USRCONF","HTCONF","TEMPORAL","URL","VBCONF","NNCONF","POSITIVE","NEGATIVE"]
symbols = [",",".","!",":",";","'","-","_","*","&","/"]

def cleanAndLowercaseToken(token):
	for symbol in symbols:
		token = token.replace(symbol,"").lower()
	return token

def initialize_feature_dict():
	feature_vector = {}
	tweet_dict = {}
	for name in feature_vector_names:
		tweet_dict[name] = False
	return tweet_dict


# Funtion to return feature dict of the tweet
# Input: a single tweet
# Output: feature dict
def prepare_feature_train(tweet):
	global tweet_feature_list_train
	label = ""
	count = 1
	tweet_id = copy.copy(count)
	count = count + 1
	tweet_dict = initialize_feature_dict()
	tokens = tweet.split()
	for token in tokens:
		if token.find("/") != -1:
			token1 = token.split("/")
			if token1[1] in tweet_dict:
				tweet_dict[token1[1]]=True
		if token.find("LABEL") != -1:
			label = "POS"
		else:
			label = "NEG"
	tweet_vector = (tweet_dict,label)
	return tweet_vector
	# tweet_feature_list_train.append(tweet_vector)

def prepare_feature_test(tweet):
	global tweet_feature_list_test
	label = None
	count = 1
	tweet_id = copy.copy(count)
	count = count + 1
	tweet_dict = initialize_feature_dict()
	tokens = tweet.split()
	for token in tokens:
		if token.find("/") != -1:
			token1 = token.split("/")
			if token1[1] in tweet_dict:
				tweet_dict[token1[1]]=True
		if token.find("LABEL") != -1:
			label = "POS"
		else:label = "NEG"
	tweet_vector = (tweet_dict,label)
	return tweet_vector
	


def load_tweets_train():
	global tweet_feature_list_test,tweet_feature_list_train
	f1 = open('tagged_tweets_feature_train.txt','r+')
	for id,tweet in enumerate(f1):
		if len(tweet) > 0 and tweet != '':
			tweet_vector = prepare_feature_train(tweet)
			tweet_feature_list_train.append(tweet_vector)
	# print tweet_feature_list_train
	return tweet_feature_list_train


def load_tweets_test():
	f1 = open('tagged_tweets_feature_test.txt','r+')
	for id,tweet in enumerate(f1):
		if len(tweet) > 0 and tweet != '':
			tweet_vector = prepare_feature_test(tweet)
			tweet_feature_list_test.append(tweet_vector)
	# print tweet_feature_list_test
	return tweet_feature_list_test
