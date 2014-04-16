import os, urllib, logging

from google.appengine.api import memcache

import jinja2
import webapp2

from dbmodel import Twiteet, HotWord
from config import tweetsonheatmap, numhotwords, numticks

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class MainPage(webapp2.RequestHandler):

	def scale(self, appearance, maxappearance):
		return appearance * 15 / maxappearance

	def hotwords():
		hotwords = {}
		words = sorted([(word, stats[word]['appearance']) for word in stats], key = lambda x : x[1], reverse = True)[:numhotwords]
		for word in words:
			hotwords[word[0]] = self.scale(word[1], words[0][1])
		memcache.set(key = "hotwords", value = hotwords)

		unitSeconds = int((timerange_high - timerange_low).total_seconds() / (numticks - 1))
		# print 'unitSeconds:', type(unitSeconds), unitSeconds
		for word in stats:
			stats[word]['ticks'] = [0 for i in range(numticks)]

			for created_at in stats[word]['created_ats']:
				stats[word]['ticks'][self.toticks(created_at, timerange_low, unitSeconds)] += 1
		
		logging.info("HotWord.query().count(): " + str(HotWord.query().count()))
		ndb.delete_multi(HotWord.query().iter(keys_only=True))
		logging.info("HotWord.query().count(): " + str(HotWord.query().count()))

		
		pass

	def get(self):
		keyword = self.request.get("query")
		if keyword != '':
			latlngs = memcache.get(keyword + "latlngs")
			tweets = memcache.get(keyword + "tweets")
			ticks = memcache.get(keyword + "ticks")
			if latlngs is None or tweets is None or ticks is None:
				record = HotWord.query(HotWord.word == keyword).get()
				if record:
					latlngs = [x.split(",") for x in record.latlngs.split(";")]
					tweets = [x.replace(keyword, "<strong>" + keyword + "</strong>") for x in record.tweets.split(";")]
					ticks = []
				else:
					latlngs = []
					tweets = []
				memcache.add(key = keyword + "latlngs", value = latlngs)
				memcache.add(key = keyword + "tweets", value = tweets)
		else:
			latlngs = memcache.get('all_latlngs')
			tweets = memcache.get('all_tweets')
			if latlngs is None or tweets is None:
				tweets = Twiteet.query().fetch(tweetsonheatmap)
				logging.info("tweets from DataStore:", tweets)
				latlngs = [(x.latitude, x.longitude) for x in tweets]
				tweets = [x.text for x in tweets[:100]]
				memcache.add(key = "all_latlngs", value = latlngs)
				memcache.add(key = "all_tweets", value = tweets)
		logging.info("keyword:[" + keyword + "]")
		logging.info("latlngs:" + str(latlngs))
		logging.info("tweets:" + str(tweets))
		
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
		self.response.write(template.render(words = hotwords, latlngs = latlngs, tweets = tweets, ticks = ticks))

	def post(self):
		logging.info("DataStore get called")
		raise Exception("not implemented!")

application = webapp2.WSGIApplication([
	('/', MainPage)
], debug=True)