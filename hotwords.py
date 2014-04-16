import time, logging, string
from datetime import datetime

import webapp2

from google.appengine.api import memcache
from google.appengine.ext import ndb

from config import auth, EC2, tweetsonheatmap, numhotwords
from dbmodel import Twiteet, APPStatus, HotWord

class Hotwords(webapp2.RequestHandler):
	def scale(self, appearance, maxappearance):
		return appearance * 15 / maxappearance

	def toticks(self, created_at, timerange_low, unitSeconds):
		return int((created_at - timerange_low).total_seconds() / unitSeconds)

	def get(self):
		logging.info("Hotwords get called")
		stopwords = set([
			'rt', 'today', "didn't", "don't",
			'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 
			'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 
			'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 
			'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 
			'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 
			'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 
			'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 
			'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 
			'with', 'about', 'against', 'between', 'into', 'through', 'during', 
			'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
			'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 
			'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 
			'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
			'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 
			't', 'can', 'will', 'just', 'don', 'should', 'now',
			])
		# tweets = Twiteet.query().fetch(100)
		tweets = Twiteet.query().fetch(tweetsonheatmap)
		stats = dict()
		timerange_low = None
		timerange_high = None
		for tweet in tweets:
			if timerange_low is None or tweet.created_at < timerange_low:
				timerange_low = tweet.created_at
			if timerange_high is None or tweet.created_at > timerange_high:
				timerange_high = tweet.created_at

			for word in tweet.text.split():
				word = word.lower()
				if word in string.punctuation or word in stopwords:
					continue
				if word not in stats:
					stats[word] = dict()
					stats[word]['latlngs'] = []
					stats[word]['created_ats'] = []
					stats[word]['tweets'] = []
					stats[word]['appearance'] = 0
				stats[word]['latlngs'].append((tweet.latitude, tweet.longitude))
				stats[word]['created_ats'].append(tweet.created_at)
				stats[word]['tweets'].append(tweet.text)
				stats[word]['appearance'] += 1
		
		numTicks = 20
		
		hotwords = {}
		words = sorted([(word, stats[word]['appearance']) for word in stats], key = lambda x : x[1], reverse = True)[:numhotwords]
		for word in words:
			hotwords[word[0]] = self.scale(word[1], words[0][1])
		memcache.set(key = "hotwords", value = hotwords)

		unitSeconds = int((timerange_high - timerange_low).total_seconds() / (numTicks - 1))
		# print 'unitSeconds:', type(unitSeconds), unitSeconds
		for word in stats:
			stats[word]['ticks'] = [0 for i in range(numTicks)]

			for created_at in stats[word]['created_ats']:
				stats[word]['ticks'][self.toticks(created_at, timerange_low, unitSeconds)] += 1
		
		logging.info("HotWord.query().count(): " + str(HotWord.query().count()))
		ndb.delete_multi(HotWord.query().iter(keys_only=True))
		logging.info("HotWord.query().count(): " + str(HotWord.query().count()))

		for word in stats:
			HotWord(word = word, 
				latlngs = ';'.join([str(x[0]) + ',' + str(x[1]) for x in stats[word]['latlngs']]), 
				tweets = ';'.join([x.replace(';', ' ') for x in stats[word]['tweets']]), 
				ticks = ';'.join([str(x) for x in stats[word]['ticks']]),
				appearance = stats[word]['appearance']
				).put()

		self.response.write("Hotwords get called")


app = webapp2.WSGIApplication([
	('/hotwords', Hotwords)
], debug=True)