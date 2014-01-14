#!/usr/bin/env python
'''
Script to modify word corpus to lowercase, strip symbols,
and remove more than one occurances
'''

file = open("Data/words.txt")
out_file = open("Data/words_clean_corpus.txt","w")
words = []
symbols = [",",".","!",":",";","'","-","_","*","&","/","?"]

def cleanAndLowercaseToken(token):
	for symbol in symbols:
		token = token.strip(symbol).lower()
	return token


for line in file:
	line = cleanAndLowercaseToken(line.split()[0])
	if line not in words:
		words.append(line)

out_file.write("\n".join(word for word in words))
print len(words)