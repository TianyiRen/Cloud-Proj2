import time, logging
from datetime import datetime

import webapp2

from google.appengine.api import memcache

from config import auth, EC2, tweetsonheatmap
from dbmodel import Twiteet, APPStatus

def twitter_time_to_datetime(twittertime):
	# example: 'Wed Apr 09 03:57:34 +0000 2014'
	t = time.strptime(twittertime, '%a %b %d %H:%M:%S +0000 %Y')
	dt = datetime.fromtimestamp(time.mktime(t))
	return dt

def fetch():
	with open("twitter-data0.txt") as tweets:
		for tweet in tweets:
			tweet = tweet.split(',')
			longitude, latitude, created_at, text = tweet[0], tweet[1], tweet[2], ' '.join(tweet[3:])
			yield longitude, latitude, twitter_time_to_datetime(created_at), text

class Warmup(webapp2.RequestHandler):

	def get(self):
		logging.info("Warmup get called")

		for longitude, latitude, created_at, text in fetch():
			Twiteet(longitude = float(longitude), latitude = float(latitude), created_at = created_at, text = text).put()

		self.response.write("Warmup get called")


app = webapp2.WSGIApplication([
	('/warmup', Warmup)
], debug=True)