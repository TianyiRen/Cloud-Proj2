from google.appengine.ext import ndb

class Twiteet(ndb.Model):
	longitude = ndb.FloatProperty(indexed=False)
	latitude = ndb.FloatProperty(indexed=False)
	created_at = ndb.DateTimeProperty()
	text = ndb.StringProperty(indexed=False)
	added_at = ndb.DateTimeProperty(auto_now_add = True, indexed=False)

class APPStatus(ndb.Model):
	datano = ndb.IntegerProperty(indexed=False)
	timerange_low = ndb.DateTimeProperty(indexed=False)
	timerange_high = ndb.DateTimeProperty(indexed=False)

class HotWord(ndb.Model):
	word = ndb.StringProperty()
	latlngs = ndb.TextProperty(indexed=False)
	tweets = ndb.TextProperty(indexed=False)
	created_ats = ndb.TextProperty(indexed=False)
	appearance = ndb.IntegerProperty()