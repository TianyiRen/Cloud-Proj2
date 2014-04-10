import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2
import twitter

# parse the tweets and store in datastore
# get
# 1. location
# 2. set of key words from content of tweets 

TWEETSTORE_NAME = 'tweet100M_store'

with open('tweets100M.txt', 'r') as tweet_data:
	for tweet in tweet_data:
		coordinates = tweet['']


def tweetstore_key(tweetstore_name=TWEETSTORE_NAME):
    """Constructs a Datastore key for parsed tweets with tweetstore_name."""
    return ndb.Key('TweetStore', tweetstore_name)

class Greeting(ndb.Model):
	"""Models an individual Guestbook entry with author, content, and date."""
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)


try:


except Exception, e:
	print e