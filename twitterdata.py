import sys, time, json, string

from twitter import *

from auth import auth

def isValidTweet(tweet):
	if not tweet or 'delete' in tweet or 'limit' in tweet or 'warning' in tweet:
		return False
	return 'coordinates' in tweet and tweet['coordinates'] \
		and 'coordinates' in tweet['coordinates'] and tweet['coordinates']['coordinates'] \
		and 'created_at' in tweet and tweet['created_at'] \
		and 'text' in tweet and tweet['text']

def tweetrecord(tweet):
	return ','.join([str(tweet['coordinates']['coordinates'][0]), str(tweet['coordinates']['coordinates'][1]), tweet['created_at'], \
		filter(lambda x: x in string.printable, tweet['text'].replace('\n', ' '))])

if __name__ == "__main__":
	# auth = OAuth(
	#     token='1673455951-jdJJJEtQJl4tCJEu0SvlWWv6XMEQ8BmEypFdUBH',
	#     token_secret='JJyDgffBQwvKl2GfwowL8xnqZqY9Sw9WeSRTOGlk679LS',
	#     consumer_key='yiVNsD8FzcsruSBpdDpRAfoqx',
	#     consumer_secret='JW4lBqpUQI2BXKDl1xc01YKBCRiDWW2IlDsZ1t6pKsiHHyACBY'
	# )

	stream = TwitterStream(auth = auth)

	waittime = 10
	datano = 0
	tweetno = 0
	MAXTWEET = 100
	starttime = time.time()
	while True:
		try:
			time.sleep(waittime)
			tweet_iter = stream.statuses.sample()
			with open("twitter-data" + str(datano) + ".txt", "a+") as tweet_data:
				for tweet in tweet_iter:
					# print "a tweet comes"
					if isValidTweet(tweet):
						# print tweetno, "a valid tweet!!"
						try:
							tweet_data.write(tweetrecord(tweet) + '\n')
						except Exception, e:
							print >> sys.stderr, e
							continue
						tweetno += 1
						if tweetno >= MAXTWEET:
							print time.time() - starttime, 'seconds before the', MAXTWEET, "tweets comes"
							starttime = time.time()
							datano += 1
							tweetno = 0
							break
		except Exception, e:
			print >> sys.stderr, e
			waittime = min(2 * waittime, 360)
			continue