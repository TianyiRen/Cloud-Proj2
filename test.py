def fetchEC2():
	import urllib2
	from config import EC2
	response = urllib2.urlopen('http://' + EC2 + '/twitter-data0.txt')
	tweets = response.read().strip().split("\n")
	for tweet in tweets:
		tweet = tweet.split(',')
		longitude, latitude, created_at, text = tweet[0], tweet[1], tweet[2], ' '.join(tweet[3:])
		print longitude, latitude, created_at, text


if __name__ == "__main__":
	fetchEC2()