import os, sys, time
import json
import logging

from twitter import *

from dbmodel import Twiteet, TwitterUser
import jinja2
import webapp2

from google.appengine.api import taskqueue
from google.appengine.ext import ndb

from auth import auth

class DataStore(webapp2.RequestHandler):

	def get(self):
		logging.info("DataStore get called")
		stream = TwitterStream(auth = auth)
		authorlist = [line.strip() for line in open("authorlist.txt")]

		# print authorlist

		while True:
			logging.info("in the while loop")
			try:
				tweet_iter = stream.statuses.filter(**{'track': ','.join(authorlist)})
				with open("twitter-data.txt", "a") as tweet_data:
					for tweet in tweet_iter:
						if tweet and 'lang' in tweet and tweet['lang'] == 'en':
							tweet_data.write(json.dumps(tweet) + "\n")
						logging.info("one tweet has arrived!")
						print "here here"
						time.sleep(3)
				logging.info("outside of open")
			except Exception, e:
				logging.info("there is exception")
				print >> sys.stderr, e
				continue
		logging.info("out of the while loop")
		self.response.write("DataStore get called")


app = webapp2.WSGIApplication([
	('/gaedatastore', DataStore)
], debug=True)