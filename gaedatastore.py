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

def fetchEC2(datano):
	import urllib2
	response = urllib2.urlopen('http://' + EC2 + '/twitter-data' + str(datano) + '.txt')
	tweets = response.read().strip().split("\n")
	for tweet in tweets:
		tweet = tweet.split(',')
		longitude, latitude, created_at, text = tweet[0], tweet[1], tweet[2], ' '.join(tweet[3:])
		yield longitude, latitude, twitter_time_to_datetime(created_at), text

class DataStore(webapp2.RequestHandler):

	def get(self):
		logging.info("DataStore get called")
		status = APPStatus.query().get()
		if not status:
			status = APPStatus(datano = 0)
		datano = status.datano

		for longitude, latitude, created_at, text in fetchEC2(datano):
			Twiteet(longitude = float(longitude), latitude = float(latitude), created_at = created_at, text = text).put()
		status.datano += 1
		status.put()
		
		latlngs = [(x.latitude, x.longitude) for x in Twiteet.query().fetch(tweetsonheatmap)]
		memcache.set(key = "latlngs", value = latlngs)

		self.response.write("DataStore get called")


app = webapp2.WSGIApplication([
	('/gaedatastore', DataStore)
], debug=True)