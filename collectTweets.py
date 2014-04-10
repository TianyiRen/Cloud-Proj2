import os
import sys, time
import json

from twitter import *

from auth import auth

# collect 100M tweets and write into file
try:
	# stream status
	twitter_stream = TwitterStream(auth=auth)
	iterator = twitter_stream.statuses.sample()
	with open('tweets100M.txt', 'w+') as tweet_data:
            for tweet in iterator:
                if tweet and 'lang' in tweet and tweet['lang'] == 'en' and tweet['coordinates']:
                    tweet_data.write(json.dumps(tweet) + "\n")
                filesize = os.path.getsize('tweets100M.txt') >> 20
                if filesize >= 100:
                    break
except Exception, e:
		print e
