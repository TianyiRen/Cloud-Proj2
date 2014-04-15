import os, urllib, logging

from google.appengine.api import memcache

import jinja2
import webapp2

from dbmodel import Twiteet, HotWord
from config import tweetsonheatmap, numhotwords

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class MainPage(webapp2.RequestHandler):

	def scale(self, appearance, maxappearance):
		return appearance * 15 / maxappearance

	def get(self):
		keyword = self.request.get("query")

		if keyword is not None:
			latlngs = memcache.get(keyword + "latlngs")
			tweets = memcache.get(keyword + "tweets")
			if latlngs is None or tweets is None:
				record = HotWord.query(HotWord.word == keyword).get()
				if record:
					latlngs = [x.split(",") for x in record.latlngs.split(";")]
					tweets = [x for x in record.tweets.split(";")]
				else:
					latlngs = []
					tweets = []
				memcache.add(key = keyword + "latlngs", value = latlngs)
				memcache.add(key = keyword + "tweets", value = tweets)
		else:
			latlngs = memcache.get('latlngs')
			tweets = []
			if latlngs is None:
				latlngs = [(x.latitude, x.longitude) for x in Twiteet.query().fetch(tweetsonheatmap)]
				memcache.add(key = "latlngs", value = latlngs)
		
		logging.info(keyword)
		logging.info(latlngs)
		logging.info(tweets)
		
		hotwords = memcache.get('hotwords')
		if hotwords is None:
			words = HotWord.query().order(-HotWord.appearance).fetch(numhotwords)

			hotwords = {}
			for word in words:
				hotwords[word.word] = self.scale(word.appearance, words[0].appearance)
			memcache.add(key = "hotwords", value = hotwords)
		# for word in hotwords:
			# logging.info(word + ":" + str(hotwords[word]))
			# words = {'hello' : 40, 'world' : 20, 'this'  : 10, 'is' : 10, 'my' : 10, 'time' : 40, 'Here': 10, 'whatistheworld' : 20}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(words = hotwords, latlngs = latlngs, tweets = tweets))

	def post(self):
		logging.info("DataStore get called")
		raise Exception("non implemented!")

application = webapp2.WSGIApplication([
	('/', MainPage)
	# ('/query', QueryMode),
], debug=True)