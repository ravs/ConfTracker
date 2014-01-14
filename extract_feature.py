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
tweet_feature_list = []

# Include POS tags in the list as per feature vector
feature_vector_names = ["NNCONF","VBCONF","USRCONF","JJCONF","CONFACRO","HTCONF","INCONF","TEMPORAL","URL"]

symbols = [",",".","!",":",";","'","-","_","*","&","/"]

def cleanAndLowercaseToken(token):
	for symbol in symbols:
		token = token.replace(symbol,"").lower()
	return token

def initialize_feature_dict():
	feature_vector = {}
	label = 0
	for name in feature_vector_names:
		feature_vector[name] = {"tokens":[]}
	tweet_dict = {"feature_vector": feature_vector, "label": label}
	return tweet_dict


# Funtion to return feature dict of the tweet
# Input: a single tweet
# Output: feature dict
def prepare_feature(tweet):
	#global tweet_feature_list
	count = 1
	tweet_id = copy.copy(count)
	count = count + 1
	tweet_dict = initialize_feature_dict()
	tokens = tweet.split()
	for token in tokens:
		if token.find("/") != -1 and token.find("CONF") != -1:
			token = token.split("/")
			print token
			if token[1] in tweet_dict["feature_vector"]:
				print token[1]
				tweet_dict["feature_vector"][token[1]]["tokens"].append(token[0])
	tweet_feature_list.append({tweet_id: tweet_dict})


if __name__=="__main__":
	prepare_feature("#CFP/HTCONF TPMCC/CONFACRO 2014  The/INCONF International/JJCONF Workshop/NNCONF on/INCONF Trusted Platforms for/INCONF Mobile/NNCONF and/INCONF Cloud Computing/VBCONF http//tco/wCCenu8BW9")
	print tweet_feature_list
	print json.dumps(tweet_feature_list)