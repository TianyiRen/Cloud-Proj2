import os, urllib, logging, time
from datetime import datetime, timedelta

from google.appengine.api import memcache

import jinja2
import webapp2

from dbmodel import Twiteet, HotWord
from config import tweetsonheatmap, numhotwords, numticks

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

def strtodatetime(timestr):
	# example: '2014-04-12 01:26:23'
	t = time.strptime(timestr, '%Y-%m-%d %H:%M:%S')
	dt = datetime.fromtimestamp(time.mktime(t))
	return dt


class MainPage(webapp2.RequestHandler):

	def scale(self, appearance, maxappearance):
		return appearance * 15 / maxappearance

	def toticks(self, created_at, timerange_low, unitSeconds):
		return int((created_at - timerange_low).total_seconds() / unitSeconds)

	def created_ats_to_ticks(self, created_ats):
		timerange_low = min(created_ats)
		timerange_high = max(created_ats)
		# logging.info("timerange_low:" + str(timerange_low))
		# logging.info("timerange_high:" + str(timerange_high))
		unitSeconds = int((timerange_high - timerange_low).total_seconds() / (numticks - 1)) + 1
		
		cnts = [0 for i in range(numticks)]
		
		for created_at in created_ats:
			# logging.info("created_at:" + str(created_at))
			# logging.info("self.toticks(created_at, timerange_low, unitSeconds):" + str(self.toticks(created_at, timerange_low, unitSeconds)))
			cnts[self.toticks(created_at, timerange_low, unitSeconds)] += 1

		ticks = {}
		delta = timedelta(seconds = unitSeconds)
		for i in range(numticks):
			ticks[timerange_low + timedelta(seconds = i * unitSeconds)] = cnts[i]
		return ticks

	def get(self):
		keyword = self.request.get("query")
		if keyword != '':
			keyword = keyword.lower()
			latlngs = memcache.get(keyword + "latlngs")
			tweets = memcache.get(keyword + "tweets")
			ticks = memcache.get(keyword + "ticks")
			if latlngs is None or tweets is None or ticks is None:
				record = HotWord.query(HotWord.word == keyword).get()
				if record:
					latlngs = [x.split(",") for x in record.latlngs.split(";")]
					tweets = [x.replace(keyword, "<strong>" + keyword + "</strong>") for x in record.tweets.split(";")]
					ticks = self.created_ats_to_ticks([strtodatetime(x) for x in record.created_ats.split(";")])
				else:
					latlngs = []
					tweets = []
				memcache.add(key = keyword + "latlngs", value = latlngs)
				memcache.add(key = keyword + "tweets", value = tweets)
				memcache.add(key = keyword + "ticks", value = ticks)
		else:
			latlngs = memcache.get('all_latlngs')
			tweets = memcache.get('all_tweets')
			ticks = memcache.get('all_ticks')
			if latlngs is None or tweets is None or ticks is None:
				tweets = Twiteet.query().fetch(tweetsonheatmap)
				latlngs = [(x.latitude, x.longitude) for x in tweets]
				ticks = self.created_ats_to_ticks([x.created_at for x in tweets])
				tweets = [x.text for x in tweets[:100]]
				memcache.add(key = "all_latlngs", value = latlngs)
				memcache.add(key = "all_tweets", value = tweets)
				memcache.add(key = "all_ticks", value = ticks)

		logging.info("keyword:[" + keyword + "]")
		# logging.info("latlngs:" + str(latlngs))
		# logging.info("tweets:" + str(tweets))
		# logging.info("ticks:" + str(ticks))
		
		hotwords = memcache.get('hotwords')
		if hotwords is None:
			words = HotWord.query().order(-HotWord.appearance).fetch(numhotwords)

			hotwords = {}
			for word in words:
				hotwords[word.word] = self.scale(word.appearance, words[0].appearance)
			memcache.add(key = "hotwords", value = hotwords)

		# for word in hotwords:
			# logging.info(word + ":" + str(hotwords[word]) + "||" + str('#' in word or '&' in word))
			# words = {'hello' : 40, 'world' : 20, 'this'  : 10, 'is' : 10, 'my' : 10, 'time' : 40, 'Here': 10, 'whatistheworld' : 20}

		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(words = hotwords, latlngs = latlngs, tweets = tweets, ticks = ticks or {}))

	def post(self):
		logging.info("DataStore get called")
		raise Exception("not implemented!")

application = webapp2.WSGIApplication([
	('/', MainPage)
], debug=True)