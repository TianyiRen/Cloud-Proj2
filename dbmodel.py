from google.appengine.ext import ndb

class Twiteet(ndb.Model):
	longitude = ndb.FloatProperty()
	latitude = ndb.FloatProperty()
	created_at = ndb.DateTimeProperty()
	text = ndb.StringProperty()
	added_at = ndb.DateProperty(auto_now_add = True)

class APPStatus(ndb.Model):
	datano = ndb.IntegerProperty()

class HotWord(ndb.Model):
	word = ndb.StringProperty()
	latlngs = ndb.TextProperty()
	tweets = ndb.TextProperty()
	ticks = ndb.TextProperty()
	appearance = ndb.IntegerProperty()