import time
import ConfigParser
import json
from twitter import *

config = ConfigParser.RawConfigParser()
config.read('keys.cfg')

CONSUMER_KEY = config.get('OAuth', 'API key')
CONSUMER_SECRET = config.get('OAuth', 'API secret')
OAUTH_TOKEN = config.get('OAuth', 'Access token')
OAUTH_TOKEN_SECRET = config.get('OAuth', 'Access token secret')

auth = OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# auth = OAuth(
#     token='1673455951-jdJJJEtQJl4tCJEu0SvlWWv6XMEQ8BmEypFdUBH',
#     token_secret='JJyDgffBQwvKl2GfwowL8xnqZqY9Sw9WeSRTOGlk679LS',
#     consumer_key='yiVNsD8FzcsruSBpdDpRAfoqx',
#     consumer_secret='JW4lBqpUQI2BXKDl1xc01YKBCRiDWW2IlDsZ1t6pKsiHHyACBY'
# )

stream = TwitterStream(auth = auth)


authorlist = [line.strip() for line in open("authorlist.txt")]
# print authorlist

tweet_iter = stream.statuses.filter(**{'track': ','.join(authorlist)})

with open("twitter-data.txt", "a") as tweet_data:
	for tweet in tweet_iter:
		if tweet['lang'] == 'en':
			tweet_data.write(json.dumps(tweet))
		time.sleep(3)