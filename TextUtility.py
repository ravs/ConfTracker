#!/usr/bin/env python
'''
Script to extract words from corpus of tweet
'''
import sys

word_list = []
symbols = [",",".","!",":",";","'","-","_","*","&","/","?","(",")","+","\"","|","$","`","~","\xe2","&amp"]

def cleanAndLowercaseToken(token):
	for symbol in symbols:
		token = token.strip(symbol).lower()
	return token

def clean_corpus(filein):
	for line in open(filein):
		line = cleanAndLowercaseToken(line.split()[0])
		if line not in word_list:
			word_list.append(line)
	filein_less_ext = filein.split(".")
	filein_less_ext.pop()
	out_file = open(".".join(filein_less_ext[:])+"_clean_corpus.txt","w")
	out_file.write("\n".join(word for word in word_list))
	print len(word_list)

def extract_words(filein):
	for line in open(filein):
		if not line:
			continue
		words = line.split()
		for word in words:
			if not word:
				continue
			word = cleanAndLowercaseToken(word)
			if word.startswith("http"):
				continue
			if len(word)<=1:
				continue
			if word not in word_list:
				word_list.append(word)
	filein_less_ext = filein.split(".")
	filein_less_ext.pop()
	out_file = open(".".join(filein_less_ext[:])+"_words.txt","w")
	out_file.write("\n".join(word for word in word_list))
	print len(word_list)

if __name__ == "__main__":
	args = sys.argv[1:]
	if not args or len(args)!=2:
		print "------------------------------------------------------\n"
		print "Usage: TextUtility.py -extractwords <tweet_corpus.txt>\nExtract words from file containing tweets to filename_words.txt\nOutput: <tweet_corpus>_words.txt"
		print "\n----------------------------------------------------\n"
		print "Usage: TextUtility.py -cleancorpus <word_corpus.txt>\nRemoves symbols, lowercase-ify words, removes redundancy from filename.txt to filename_clean_corpus.txt\nOutput: <filename>_clean_corpus.txt"
	else:
		if args[0] == "-extractwords":
			extract_words(args[1])
		elif args[0] == "-cleancorpus":
			clean_corpus(args[1])