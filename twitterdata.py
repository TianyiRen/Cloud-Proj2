import sys, time
import json

from twitter import *

# from auth import auth

auth = OAuth(
    token='1673455951-jdJJJEtQJl4tCJEu0SvlWWv6XMEQ8BmEypFdUBH',
    token_secret='JJyDgffBQwvKl2GfwowL8xnqZqY9Sw9WeSRTOGlk679LS',
    consumer_key='yiVNsD8FzcsruSBpdDpRAfoqx',
    consumer_secret='JW4lBqpUQI2BXKDl1xc01YKBCRiDWW2IlDsZ1t6pKsiHHyACBY'
)

stream = TwitterStream(auth = auth)


authorlist = [line.strip() for line in open("authorlist.txt")]
# print authorlist

waittime = 1
while True:
	try:
		time.sleep(waittime)
		waittime = min(2 * waittime, 360)
		tweet_iter = stream.statuses.filter(**{'track': ','.join(authorlist)})
		with open("twitter-data.txt", "a") as tweet_data:
			for tweet in tweet_iter:
				if tweet and 'lang' in tweet and tweet['lang'] == 'en':
					tweet_data.write(json.dumps(tweet) + "\n")
				time.sleep(3)
	except Exception, e:
		print >> sys.stderr, e
		continue