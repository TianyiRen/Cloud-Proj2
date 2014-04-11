import os, sys, time, json, logging

from datetime import datetime

from tweepy.streaming import StreamListener
from tweepy import Stream

from auth import auth

def twitter_time_to_datetime(twittertime):
	# example: 'Wed Apr 09 03:57:34 +0000 2014'
	t = time.strptime(twittertime, '%a %b %d %H:%M:%S +0000 %Y')
	dt = datetime.fromtimestamp(time.mktime(t))
	return dt

class StdOutListener(StreamListener):
	""" A listener handles tweets are the received from the stream.
	This is a basic listener that just prints received tweets to stdout.

	"""
	def on_data(self, data):
		logging.info("tweet comes!!")
		tweet = json.loads(data)
		print tweet
		print type(tweet)
		if not tweet or 'delete' in tweet or 'limit' in tweet or 'warning' in tweet:
			print >> sys.stderr, tweet
		elif 'lang' in tweet and tweet['lang'] == 'en':
			print tweet
			logging.info("tweet stored!!")
		else:
			# other language, ignore
			pass

	def on_timeout(self):
		logging.info("Timeout, sleeping for 60 seconds...")
		sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
		time.sleep(60)
		return 

	def on_error(self, status):
		logging.info("on_error:" + status)
		print >> sys.stderr, status

if __name__ == "__main__":
	logging.info("DataStore get called")
	authorlist = [line.strip() for line in open("authorlist.txt")]

	l = StdOutListener()
	stream = Stream(auth, l)
	stream.filter(track = authorlist)
	stream = TwitterStream(auth = auth)