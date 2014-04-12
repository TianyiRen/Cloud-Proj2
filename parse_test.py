import json

with open('parse_ex.txt') as tweets_file:
	for line in tweets_file:
		# print line
		# print '\n\n'
		tweet = json.loads(line)
		# location information 
		print tweet['coordinates']['coordinates']
		
		# a set of key words
		




