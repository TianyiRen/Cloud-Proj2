import os, sys, time, json, logging

from dbmodel import Twiteet, TwitterUser
import jinja2
import webapp2

from datetime import datetime

from google.appengine.api import taskqueue
from google.appengine.ext import ndb

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
	def on_data(self, tweet):
		logging.info("tweet comes!!")
		if not tweet or 'delete' in tweet or 'limit' in tweet or 'warning' in tweet:
			print >> sys.stderr, tweet
		elif 'lang' in tweet and tweet['lang'] == 'en':
			Twiteet(tweet['id'], 
				tweet['coordinates']['coordinates'][0] if 'coordinates' in tweet and tweet['coordinates'] and 'coordinates' in tweet['coordinates'] and tweet['coordinates']['coordinates'] else '', 
				tweet['coordinates']['coordinates'][1] if 'coordinates' in tweet and tweet['coordinates'] and 'coordinates' in tweet['coordinates'] and tweet['coordinates']['coordinates'] else '', 
				twitter_time_to_datetime(tweet['created_at']) if 'created_at' in tweet and tweet['created_at'] else None,
				tweet['favorite_count'] if 'favorite_count' in tweet else 0,
				tweet['retweet_count'] if 'retweet_count' in tweet else 0, 
				tweet['text'] if 'text' in tweet else '',
				tweet['user']['id_str'] if 'user' in tweet and 'id_str' in tweet['user'] else None).put()
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
	
class DataStore(webapp2.RequestHandler):

	def get(self):
		logging.info("DataStore get called")
		authorlist = [line.strip() for line in open("authorlist.txt")]

		# l = StdOutListener()
		# stream = Stream(auth, l)
		# stream.filter(track = authorlist)
		# stream = TwitterStream(auth = auth)
		with open("sampletweet.txt") as f:
			tweet = json.loads(f.read())
			# print 'tweet[id]', tweet['id']
			# print '1', tweet['coordinates']['coordinates'][0] if 'coordinates' in tweet and tweet['coordinates'] and 'coordinates' in tweet['coordinates'] and tweet['coordinates']['coordinates'] else ''
			# print '2', tweet['coordinates']['coordinates'][1] if 'coordinates' in tweet and tweet['coordinates'] and 'coordinates' in tweet['coordinates'] and tweet['coordinates']['coordinates'] else '' 
			# print '3', twitter_time_to_datetime(tweet['created_at']) if 'created_at' in tweet and tweet['created_at'] else None
			# print '4', tweet['favorite_count'] if 'favorite_count' in tweet else 0
			# print '5', tweet['retweet_count'] if 'retweet_count' in tweet else 0
			# print '6', 'text' if 'text' in tweet else ''
			# print '7', tweet['user']['id_str'] if 'user' in tweet and 'id_str' in tweet['user'] else None
			
			Twiteet(twiteetid = tweet['id_str'],
				longitude = tweet['coordinates']['coordinates'][0] if 'coordinates' in tweet and tweet['coordinates'] and 'coordinates' in tweet['coordinates'] and tweet['coordinates']['coordinates'] else '', 
				latitude = tweet['coordinates']['coordinates'][1] if 'coordinates' in tweet and tweet['coordinates'] and 'coordinates' in tweet['coordinates'] and tweet['coordinates']['coordinates'] else '', 
				created_at = twitter_time_to_datetime(tweet['created_at']) if 'created_at' in tweet and tweet['created_at'] else None,
				favorite_count = tweet['favorite_count'] if 'favorite_count' in tweet else 0,
				retweet_count = tweet['retweet_count'] if 'retweet_count' in tweet else 0, 
				text = tweet['text'] if 'text' in tweet else '',
				twitter_userid = tweet['user']['id_str'] if 'user' in tweet and 'id_str' in tweet['user'] else None).put()

		# print authorlist

		# while True:
		# 	logging.info("in the while loop")
		# 	try:
		# 		tweet_iter = stream.statuses.filter(**{'track': ','.join(authorlist)})
		# 		with open("twitter-data.txt", "a") as tweet_data:
		# 			for tweet in tweet_iter:
		# 				if tweet and 'lang' in tweet and tweet['lang'] == 'en':
		# 					tweet_data.write(json.dumps(tweet) + "\n")
		# 				logging.info("one tweet has arrived!")
		# 				print "here here"
		# 				time.sleep(3)
		# 		logging.info("outside of open")
		# 	except Exception, e:
		# 		logging.info("there is exception")
		# 		print >> sys.stderr, e
		# 		continue
		# logging.info("out of the while loop")
		self.response.write("DataStore get called")


app = webapp2.WSGIApplication([
	('/gaedatastore', DataStore)
], debug=True)