# Linying Xie umid:xly
# these should be the only imports you need
import tweepy
import nltk
import json
import sys

# write your code here
# usage should be python3 part1.py <username> <num_tweets>

CONSUMER_KEY = "pobKOLmiVGqyUeO2voQtVzoWU" 
CONSUMER_SECRET = "1ryezaI1JRrnk1eJqkVdJMEZtfewTEYhrmiVXMVM81FcQZJZkx"

ACCESS_TOKEN = "925728062267936768-5VoMvQ36TgwxsBkixFI0N2vZhQUEwJR"
ACCESS_TOKEN_SECRET = "hjLojE1Tq6Oi9yQeklUfMGBMb6NAmjzqvDgulaZZqTBas"

def access_tweets(user_name, num_of_tweets):
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)

	tweets = api.user_timeline(user_name, count = num_of_tweets, include_rts=True)
	tweet_text = [advanced_tokenize(tweet.text) for tweet in tweets]
	tweet_text = tagging(tweet_text)
	# print(tweet_text)

	origins = [tweet for tweet in tweets if not hasattr(tweet, 'retweeted_status')]
	favored_count = sum([tweet.favorite_count for tweet in origins])
	retweeted_count = sum([tweet.retweet_count for tweet in origins])

	top_verbs = sort_occurance(tweet_text, 'VB')
	top_verbs = [str(word_pair[0])+'(' + str(word_pair[1]) + ')' for word_pair in top_verbs[:5]]

	top_nouns_old = sort_occurance(tweet_text, 'NN')
	top_nouns = [str(word_pair[0])+'(' + str(word_pair[1]) + ')' for word_pair in top_nouns_old[:5]]

	top_adjectives = sort_occurance(tweet_text, 'JJ')
	top_adjectives = [str(word_pair[0])+'(' + str(word_pair[1]) + ')' for word_pair in top_adjectives[:5]]

	return [top_verbs, top_nouns, top_adjectives, len(origins), favored_count, retweeted_count, top_nouns_old]

def sort_occurance(tagged_words, POS_keyword):
	target = [word[0] for word in tagged_words if word[1][:2] == POS_keyword]

	occr_dict = dict((x, target.count(x)) for x in target)
	occr_dict = sorted(occr_dict.items())
	top_words = sorted(occr_dict, key = lambda x: x[1], reverse = True)
	# print(top_words)

	return top_words


def advanced_tokenize(sentence):
	tokens = sentence.split(' ')
	recs = [token for token in tokens if token != '' and not any(token.startswith(x) for x in ['RT', 'http', 'https']) and token[0].isalpha()]
	return recs

def tagging(word_list):
	flatten = [word for words in word_list for word in words]
	return nltk.pos_tag(flatten)

def print_output(user_name, num_of_tweets, verbs, nouns, adjectives, num_origin, num_favourit, num_retweeted, useless):
	print("USER: ", user_name)
	print("TWEETS ANALYZED: ", num_of_tweets)
	print("VERBS: ", verbs)
	print("NOUNS: ", nouns)
	print("ADJECTIVES: ", adjectives)
	print("ORINGINAL TWEETS: ", num_origin)
	print("TIMES FAVORITED (ORIGINAL TWEETS ONLY): ", num_favourit)
	print("TIMES RETWEETED (ORIGINAL TWEETS ONLY): ", num_retweeted)

def generate_csv(nouns, fname = 'noun_data.csv'):
	outfile = open(fname, "w", encoding = 'utf-8')
	header_columns = ["Noun", "Number"]  # define header
	outfile.write('{},{}\n'.format(*header_columns))
	for noun in nouns[:5]:
		outfile.write('{},{}\n'.format(*noun))
	outfile.close()

if __name__=="__main__":

	if len(sys.argv) <3:
		print("please specify both the user name and number of tweets to analyze")
	user_name = sys.argv[1]
	num_of_tweets = int(sys.argv[2])

	results = access_tweets(user_name, num_of_tweets)
	print_output(user_name, num_of_tweets, *results)
	generate_csv(results[-1])
