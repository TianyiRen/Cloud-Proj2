from google.appengine.ext import db

class Twiteet(db.model):
	twiteetid = db.StringProperty()
	longitude = db.FloatProperty()
	latitude = db.FloatProperty()
	created_at = db.DateProperty()
	favorite_count = db.IntegerProperty()
	retweet_count = db.IntegerProperty()
	text = db.StringProperty()
	twitterid = db.StringProperty()

class TwitterUser(db.model):
	twitterid = db.StringProperty()
	verified = db.BooleanProperty()
	followers_count = db.IntegerProperty()
	screen_name = db.StringProperty()
	name = db.StringProperty()