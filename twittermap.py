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
		latlngs = memcache.get('latlngs')
		if latlngs is None:
			latlngs = [(x.latitude, x.longitude) for x in Twiteet.query().fetch(tweetsonheatmap)]
			memcache.add(key = "latlngs", value = latlngs)

		# logging.info(latlngs)
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
		self.response.write(template.render(words = hotwords, latlngs = latlngs))

	def post(self):
		logging.info("DataStore get called")
		raise Exception("non implemented!")

application = webapp2.WSGIApplication([
	('/', MainPage)
	# ('/query', QueryMode),
], debug=True)