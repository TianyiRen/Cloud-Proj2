import json

# from google.appengine.ext import db

# class Twiteet(db.model):
# 	longitude = db.FloatProperty()
# 	latitude = db.FloatProperty()
# 	created_at = db.DateProperty()
# 	favorite_count = db.IntegerProperty()
# 	retweet_count = db.IntegerProperty()
# 	text = db.StringProperty()
# 	twitterid = db.StringProperty()

# class TwitterUser(db.model):
# 	twitterid = db.StringProperty()
# 	verified = db.BooleanProperty()
# 	followers_count = db.IntegerProperty()
# 	screen_name = db.StringProperty()
# 	name = db.StringProperty()

if __name__ == "__main__":
	with open("twitter-data.txt") as f:
		for t in f:
			try:
				# print "encoded:", t
				print "decoded:", json.dumps(json.loads(t), indent = 4)
			except Exception, e:
				print e
				continue