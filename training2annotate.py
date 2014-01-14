#!/usr/bin/env python
import sys
import os
import re

pos_dict = {}
symbols = [",",".","!",",",":",";","'"]

def tokenize_tweet(training_file, output_file):
	annotated_out_temp = open(output_file+".tmp", "w")
	for line in open(training_file):
		token_list = []
		line = line.strip()
		if not line:
			continue
		line = line.split(' ')
		for token in line:
			token_list.append(token)
		annotated_out_temp.write("\n".join(token for token in token_list) + "\n\n")

#Load the dict of pos for annotation
def load_dict():
	pos_dict["JJCONF"] = get_tokens("./Data/token/ADJ")
	pos_dict["NNCONF"] = get_tokens("./Data/token/NOUN")
	pos_dict["VBCONF"] = get_tokens("./Data/token/VERB")
	pos_dict["USRCONF"] = get_tokens("./Data/token/HANDLE")
	pos_dict["HTCONF"] = get_tokens("./Data/token/HASHTAG")
	pos_dict["CONFACRO"] = get_tokens("./Data/token/CONFACRO")
	pos_dict["INCONF"] = get_tokens("./Data/token/LOWER")

def get_tokens(from_file):
	tokens = []
	for line in open(from_file):
		line = line.split()
		if not line:
			continue
		if line not in tokens:
			tokens.append(line[0])
	print tokens
	return tokens

def cleanToken(token):
	for symbol in symbols:
		token = token.replace(symbol,"")
	return token

#Annotate tweet based on augmented pos dict after annotating,
#add the annotated words in the dict. Keep running this over batch
#of tweets(in our case 100 tweets).
def annotate_tweet(output_file):
	annotated_out_temp = open(output_file+".tmp")
	annotated_out = open(output_file, "w")
	for line in annotated_out_temp:
		line = line.split()
		if not line:
			annotated_out.write("\n")
			continue
		line = cleanToken(line[0])
		flag = 0
		for key in pos_dict:
			#if line in pos_dict[key] and flag == 0:
			if key == "NNCONF" or key == "HTCONF" or key == "USRCONF":
				if re.search("|".join(tag for tag in pos_dict[key]),line,re.IGNORECASE) and flag == 0:
					annotated_out.write(line+"/"+key+" ")
					flag = 1;
			elif key == "CONFACRO":
				if line.upper() in pos_dict[key] and flag == 0:
					annotated_out.write(line+"/"+key+" ")
					flag = 1;
			else: 
				if line in pos_dict[key] and flag == 0:
					annotated_out.write(line+"/"+key+" ")
					flag = 1;
		if flag == 0:
			annotated_out.write(line+" ")
	annotated_out_temp.close()
	os.remove(output_file+".tmp")

if __name__ == "__main__":
	tokenize_tweet(sys.argv[1], sys.argv[2])
	load_dict()
	annotate_tweet(sys.argv[2])