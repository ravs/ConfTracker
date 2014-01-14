import nltk
import sys
import extract_feature
import annotate_tweets

train = {}
test = {}
train_input = []
test_input = []

def prepare_classify_input(tweet):
	id_val = ""
	temporal = ""
	tweet_dict = extract_feature.initialize_feature_dict()
	tokens = tweet.split()
	for token in tokens:
		if token.find("ID:") != -1: 
			temp = token.split(":")
			id_val = temp[1]
		if token.find("/") != -1:
			token1 = token.split("/")
			if token1[1] in tweet_dict:
				tweet_dict[token1[1]]=True
		if token.find("/TEMPORAL") != -1:
			temp = token.split("/")
			temporal = temp[0]
	tweet_vector = tweet_dict
	return tweet_vector,id_val,temporal

def load_train_dict():
	global train_input,test_input
	train_input = extract_feature.load_tweets_train()
	# print train_input
	test_input = extract_feature.load_tweets_test()

def classifier_NB():
	global train_input,test_input
	roc_data = ""
	classifier = nltk.classify.NaiveBayesClassifier.train(train_input)
	# print sorted(classifier.labels())
	print nltk.classify.accuracy(classifier, test_input)
	# for pdist in classifier.batch_prob_classify(test_input):
	#  	print('%.4f %.4f' % (pdist.prob('Y'), pdist.prob('N')))


def predict_for_each_tweet(filename):
	classifier = nltk.classify.NaiveBayesClassifier.train(train_input)
	f1 = open(filename,'r+')
	f2 = open('predicted_tweets.txt','w+')
	f3 = open('conf_related_classified_tweets.txt','w+')
	annotate_tweets.load_corpus()
	for id,tweet in enumerate(f1):
		if len(tweet) > 0 and tweet != '' and tweet != '\n':
			tagged_tweet = annotate_tweets.split_words_in_tweets_i(tweet,id)
			tweet_vector,id_val,temporal = prepare_classify_input(tagged_tweet)
			label = classifier.classify(tweet_vector)
			f2.write(id_val+"->"+label+"->"+temporal +"\n")
			if label is "POS":
				f3.write("ID:"+str(id)+" "+tweet+"  Tentative calculated Date: "+temporal+"\n")
	print "Output :"
	print "Accuracy is "+str(nltk.classify.accuracy(classifier, test_input)*100)
	print """
	Open
	->conf_related_classified_tweets.txt
	->predicted_tweets.txt
	"""


def main():
	filename = sys.argv[1]
	load_train_dict()
	# classifier_NB()
	predict_for_each_tweet(filename)	

if __name__ == '__main__':
	if len(sys.argv) != 1:
		main()
	else:
		print """Please note the following Usage
First argument = Enter the filename with tweets that are to be classified.
Each tweet should be separated by a NEW LINE '\\n' character
Output :
	predicted_tweets.txt
	conf_related_classified_tweets.txt
"""