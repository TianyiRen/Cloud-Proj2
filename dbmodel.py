from google.appengine.ext import ndb

class Twiteet(ndb.Model):
	twiteetid = ndb.StringProperty()
	longitude = ndb.FloatProperty()
	latitude = ndb.FloatProperty()
	created_at = ndb.DateProperty()
	favorite_count = ndb.IntegerProperty()
	retweet_count = ndb.IntegerProperty()
	text = ndb.StringProperty()
	twitterid = ndb.StringProperty()

class TwitterUser(ndb.Model):
	twitterid = ndb.StringProperty()
	verified = ndb.BooleanProperty()
	followers_count = ndb.IntegerProperty()
	screen_name = ndb.StringProperty()
	name = ndb.StringProperty()