USRCONF_dict = {}
USRCONF_list = set()
HTCONF_dict = {}
HTCONF_list = set()
HTTECH_dict = {}
HTTECH_list = set()
CONF_dict = {}
CONF_list = set()
CONFACRO_dict = {}
CONFACRO_list = set()

def load_sets():
	global USRCONF_list,HTCONF_list,HTTECH_list,CONF_list,CONFACRO_list
	f2 = open('USRCONF_corpus.txt','r+')
	f3 = open('CONF_corpus.txt','r+')
	f4 = open('HTCONF_corpus.txt','r+')
	f5 = open('HTTECH_corpus.txt','r+')
	f6 = open('CONFACRO_corpus.txt','r+')
	for word in f2:
		word = word.rstrip('\n')
		if word not in USRCONF_list:
			USRCONF_list.add(word)
	for word in f3:
		word = word.rstrip('\n')
		if word not in HTCONF_list:
			HTCONF_list.add(word)
	for word in f4:
		word = word.rstrip('\n')
		if word not in HTTECH_list:
			HTTECH_list.add(word)
	for word in f5:
		word = word.rstrip('\n')
		if word not in CONF_list:
			CONF_list.add(word)
	for word in f6:
		word = word.rstrip('\n')
		if word not in CONFACRO_list:
			CONFACRO_list.add(word)
	f2.close()
	f3.close()
	f4.close()
	f5.close()
	f6.close()


def load_dictionary():
	global USRCONF_list,HTCONF_list,HTTECH_list,CONF_list,USRCONF_dict,HTTECH_dict,HTCONF_dict,CONF_dict,CONFACRO_list,CONFACRO_dict
	USRCONF_dict = USRCONF_list
	HTCONF_dict = HTCONF_list
	HTTECH_dict = HTTECH_list
	CONF_dict = CONF_list
	CONFACRO_dict = CONFACRO_list


def extract_tag():
	global USRCONF_list,HTCONF_list,HTTECH_list,CONF_list,CONFACRO_list
	f1 = open('ner_manual_tagging_200.txt','r+')
	# f1 = open('test.txt','r+')
	f2 = open('USRCONF_corpus.txt','a+')
	f3 = open('CONF_corpus.txt','a+')
	f4 = open('HTCONF_corpus.txt','a+')
	f5 = open('HTTECH_corpus.txt','a+')
	f6 = open('CONFACRO_corpus.txt','a+')
	for i in f1:
		temp = []
		if i.find("USRCONF") is not -1:
			temp = i.split("\t")
			temp[0] = temp[0].lower().rstrip('\n')
			USRCONF_list = list(USRCONF_list)
			if temp[0] not in USRCONF_list:
				USRCONF_list.append(temp[0])
				f2.write(str(temp[0]))
				f2.write("\n")
		if i.find("CONF") is not -1:
			temp = i.split("\t")
			temp[0] = temp[0].lower().rstrip('\n')
			CONF_list = list(CONF_list)
			if temp[0] not in CONF_list:
				CONF_list.append(temp[0])
				f3.write(str(temp[0]))
				f3.write("\n")
		if i.find("HTCONF") is not -1:
			temp = i.split("\t")
			temp[0] = temp[0].lower().rstrip('\n')
			HTCONF_list = list(HTCONF_list)
			if temp[0] not in HTCONF_list:
				HTCONF_list.append(temp[0])
				f4.write(str(temp[0]))
				f4.write("\n")
		if i.find("HTTECH") is not -1:
			temp = i.split("\t")
			temp[0] = temp[0].lower().rstrip('\n')
			HTTECH_list = list(HTTECH_list)
			if temp[0] not in HTTECH_list:
				HTTECH_list.append(temp[0])
				f5.write(str(temp[0]))
				f5.write("\n")
		if i.find("CONFACRO") is not -1:
			temp = i.split("\t")
			temp[0] = temp[0].lower().rstrip('\n')
			CONFACRO_list = list(CONFACRO_list)
			if temp[0] not in CONFACRO_list:
				CONFACRO_list.append(temp[0])
				f6.write(temp[0])
				f6.write("\n")

	f2.close()
	f3.close()
	f4.close()
	f5.close()
	f6.close()

load_sets()
load_dictionary()
extract_tag()