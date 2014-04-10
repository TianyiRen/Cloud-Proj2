import json

from dbmodel import Twiteet, TwitterUser

if __name__ == "__main__":
	with open("twitter-data.txt") as f:
		for t in f:
			try:
				# print "encoded:", t
				# print "decoded:", json.dumps(json.loads(t), indent = 4)
				json.loads(t)
			except Exception, e:
				print e
				continue