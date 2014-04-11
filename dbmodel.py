from google.appengine.ext import ndb

class Twiteet(ndb.Model):
	twiteetid = ndb.StringProperty()
	longitude = ndb.FloatProperty()
	latitude = ndb.FloatProperty()
	created_at = ndb.DateTimeProperty()
	favorite_count = ndb.IntegerProperty()
	retweet_count = ndb.IntegerProperty()
	text = ndb.StringProperty()
	twitter_userid = ndb.StringProperty()
	added_at = ndb.DateProperty(auto_now_add = True)

	def __init__(self, twiteetid, longitude, latitude, created_at, favorite_count, retweet_count, text, twitter_userid):
		self.twiteetid = twiteetid
		self.longitude = longitude
		self.latitude = latitude
		self.created_at = created_at
		self.favorite_count = favorite_count
		self.retweet_count = retweet_count
		self.text = text
		self.twitter_userid = twitter_userid

class TwitterUser(ndb.Model):
	twitter_userid = ndb.StringProperty()
	verified = ndb.BooleanProperty()
	followers_count = ndb.IntegerProperty()
	screen_name = ndb.StringProperty()
	name = ndb.StringProperty()