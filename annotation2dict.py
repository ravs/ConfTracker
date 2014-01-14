#!/usr/bin/env python

import sys

pos_dict = {}

def prepare_dict(annotated_data):
	for line in open(annotated_data):
		line = line.strip();
		if not line:
			continue
		line = line.split("\t")
		#print line
		if len(line) == 2:
			if line[1] not in pos_dict:
				pos_dict[line[1]] = []
			if line[0] not in pos_dict[line[1]]:
				pos_dict[line[1]].append(line[0])
	print pos_dict

def write_dict():
	for key in pos_dict:
		if key.startswith("NN"):
			fout = open("./token/NOUN", "a")
		elif key.startswith("JJ"):
			fout = open("./token/ADJ", "a")
		elif key.startswith("VB"):
			fout = open("./token/VERB", "a")
		elif key.startswith("PRP"):
			fout = open("./token/PREP", "a")
		elif key.startswith("HT"):
			fout = open("./token/HASHTAG", "a")
		elif key.startswith("USR"):
			fout = open("./token/HANDLE", "a")
		elif key.startswith("IN"):
			fout = open("./token/LOWER", "a")
		elif key.endswith("ACRO"):
			fout = open("./token/CONFACRO", "a")
		else:
			fout = open("./token/"+key, "a")
		fout.write("\n".join(token for token in pos_dict[key])+"\n")

if __name__ == "__main__":
	prepare_dict(sys.argv[1])
	write_dict()