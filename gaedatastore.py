import time, logging, string
from datetime import datetime

import webapp2

from google.appengine.api import memcache

from config import auth, EC2, tweetsonheatmap, numticks, stopwords, numhotwords
from dbmodel import Twiteet, APPStatus, HotWord

def twitter_time_to_datetime(twittertime):
	# example: 'Wed Apr 09 03:57:34 +0000 2014'
	t = time.strptime(twittertime, '%a %b %d %H:%M:%S +0000 %Y')
	dt = datetime.fromtimestamp(time.mktime(t))
	return dt

def fetchEC2(datano):
	import urllib2
	response = urllib2.urlopen('http://' + EC2 + '/twitter-data' + str(datano) + '.txt')
	tweets = response.read().strip().split("\n")
	for tweet in tweets:
		tweet = tweet.split(',')
		longitude, latitude, created_at, text = tweet[0], tweet[1], tweet[2], ' '.join(tweet[3:])
		yield longitude, latitude, twitter_time_to_datetime(created_at), text

class DataStore(webapp2.RequestHandler):

	def get(self):
		logging.info("DataStore get called")

		status = APPStatus.query().get()
		if not status:
			status = APPStatus(datano = 0, timerange_low = datetime.now(), timerange_high = datetime.now())
		datano = status.datano

		newlatlngs = []
		stats = dict()

		timerange_low = status.timerange_low
		timerange_high = status.timerange_high

		for longitude, latitude, created_at, text in fetchEC2(datano):
			longitude, latitude = float(longitude), float(latitude)
			Twiteet(longitude = longitude, latitude = latitude, created_at = created_at, text = text).put()
			
			newlatlngs.append((latitude, longitude))


			if timerange_low is None or created_at < timerange_low:
				timerange_low = created_at
			if timerange_high is None or created_at > timerange_high:
				timerange_high = created_at

			for word in text.split():
				word = word.lower().replace("(", "").replace(")", "")
				if word in string.punctuation or word in stopwords or word.startswith("http"):
					continue
				# word = word.replace('#', '').replace('&', '')
				if word not in stats:
					stats[word] = dict()
					stats[word]['latlngs'] = []
					stats[word]['created_ats'] = []
					stats[word]['tweets'] = []
					stats[word]['appearance'] = 0
				stats[word]['latlngs'].append((latitude, longitude))
				stats[word]['created_ats'].append(created_at)
				stats[word]['tweets'].append(text)
				stats[word]['appearance'] += 1

		status.datano += 1
		status.timerange_low = timerange_low
		status.timerange_high = timerange_high
		status.put()

		latlngs = memcache.get('all_latlngs')
		if latlngs:
			latlngs = latlngs[: -len(newlatlngs)] + newlatlngs
			# logging.info("len(latlngs):" + str(len(latlngs)))
			memcache.set(key = "all_latlngs", value = latlngs)


		for word in stats:
			record = HotWord.query(HotWord.word == word).get()
			if record:
				record.latlngs += ";" + ';'.join([str(x[0]) + ',' + str(x[1]) for x in stats[word]['latlngs']])
				record.tweets += ";" + ';'.join([x.replace(';', ' ') for x in stats[word]['tweets']])
				if record.created_ats is None:
					record.created_ats = ""
				else:
					record.created_ats += ";" 
				record.created_ats += ';'.join([str(x) for x in stats[word]['created_ats']])

				record.appearance += stats[word]['appearance']
				stats[word]['appearance'] = record.appearance
			else:
				record = HotWord(word = word, 
				latlngs = ';'.join([str(x[0]) + ',' + str(x[1]) for x in stats[word]['latlngs']]), 
				tweets = ';'.join([x.replace(';', ' ') for x in stats[word]['tweets']]), 
				created_ats = ';'.join([str(x) for x in stats[word]['created_ats']]),
				appearance = stats[word]['appearance']
				)
			record.put()

		hotwords = memcache.get("hotwords")
		if hotwords is not None:
			for word in stats:
				hotwords[word] = stats[word]['appearance']

			newhotwords = {}
			for w, c in sorted([(w, hotwords[w]) for w in hotwords], key = lambda x : x[1], reverse = True)[:numhotwords]:
				newhotwords[w] = c
			memcache.set(key = "hotwords", value = newhotwords)

		self.response.write("DataStore get called")


app = webapp2.WSGIApplication([
	('/gaedatastore', DataStore)
], debug=True)