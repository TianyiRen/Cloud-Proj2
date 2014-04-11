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
		else:
			# other language, ignore
			pass

	def on_timeout(self):
		sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
		time.sleep(60)
		return 

	def on_error(self, status):
		print >> sys.stderr, status