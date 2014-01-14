#!/usr/bin/env python

'''
Python script to extract features from tweet corpus in libsvm format
'''

import sys

# List of tweets with corresponding feature vector and label
# tweet_feature_list = 
#[
# 1 w1:1 w2:1 w3:1
# 1 w200:1 w222:1
# -1 wXXX:1 wZZZ:1 
#]
tweet_feature_positive_list = []
tweet_feature_negative_list = []

word_corpus = open("Data/conf_training_set_words.txt")
train = open("Data/test_svm_400_2.dat","w")

symbols = [",",".","!",":",";","'","-","_","*","&","/","?","(",")","+","\"","|","$","`","~","\xe2","&amp"]

def cleanAndLowercaseToken(token):
	for symbol in symbols:
		token = token.replace(symbol,"").lower()
	return token

def prepare_feature_libsvm_format(tweet):
	tokens = tweet.split()
	placeholder = tokens.pop() # get the label value from the last token
	feat_val_dict = {}
	line_num = 0
	print tokens
	for token in tokens:
		token = cleanAndLowercaseToken(token)
		if token.startswith("http"):
			continue
		if len(token)<=1:
			continue
		word_corpus.seek(0)
		line_num = 0
		for line in word_corpus:
			line_num = line_num + 1
			if token == line.split()[0]:
				feat_val_dict[line_num] = 1
				#placeholder = placeholder + " " + str(line_num) + ":" + str(1)
	for key in sorted(feat_val_dict):
		placeholder = placeholder + " " + str(key) + ":" + str(feat_val_dict[key])
	return placeholder

if __name__=="__main__":
	print prepare_feature_libsvm_format("#CFP TPMCC 2014  The International Workshop on Trusted Platforms for Mobile and Cloud Computing http//tco/wCCenu8BW9	1")
	for line in open(sys.argv[1]):
		tweet_feature = prepare_feature_libsvm_format(line)
		print tweet_feature
		if tweet_feature.startswith("1"):
			tweet_feature_positive_list.append(tweet_feature)
		elif tweet_feature.startswith("-1"):
			tweet_feature_negative_list.append(tweet_feature)
	train.write("\n".join(line for line in tweet_feature_positive_list)+"\n")
	train.write("\n".join(line for line in tweet_feature_negative_list))
