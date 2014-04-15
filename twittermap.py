import os, urllib, logging

from google.appengine.api import memcache

import jinja2
import webapp2

from dbmodel import Twiteet
from config import tweetsonheatmap

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class MainPage(webapp2.RequestHandler):

	def get(self):
		latlngs = memcache.get('latlngs')
		if latlngs is None:
			latlngs = [(x.latitude, x.longitude) for x in Twiteet.query().fetch(tweetsonheatmap)]
			memcache.add(key = "latlngs", value = latlngs)

		logging.info(latlngs)
		words = {'hello' : 40, 'world' : 20, 'this'  : 10, 'is' : 10, 'my' : 10, 'time' : 40, 'Here': 10, 'whatistheworld' : 20}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(words = words, latlngs = latlngs))

	def post(self):
		logging.info("DataStore get called")
		raise Exception("non implemented!")

application = webapp2.WSGIApplication([
	('/', MainPage)
	# ('/query', QueryMode),
], debug=True)