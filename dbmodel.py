from google.appengine.ext import ndb

class Twiteet(ndb.Model):
	longitude = ndb.FloatProperty()
	latitude = ndb.FloatProperty()
	created_at = ndb.DateTimeProperty()
	text = ndb.StringProperty()
	added_at = ndb.DateTimeProperty(auto_now_add = True)

class APPStatus(ndb.Model):
	datano = ndb.IntegerProperty()
	timerange_low = ndb.DateTimeProperty()
	timerange_high = ndb.DateTimeProperty()

class HotWord(ndb.Model):
	word = ndb.StringProperty()
	latlngs = ndb.TextProperty()
	tweets = ndb.TextProperty()
	created_ats = ndb.TextProperty()
	appearance = ndb.IntegerProperty()