import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('keys.cfg')

CONSUMER_KEY = config.get('OAuth', 'API key')
CONSUMER_SECRET = config.get('OAuth', 'API secret')
OAUTH_TOKEN = config.get('OAuth', 'Access token')
OAUTH_TOKEN_SECRET = config.get('OAuth', 'Access token secret')

from twitter import OAuth
auth = OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

EC2 = config.get('EC2', 'server')

# from tweepy import OAuthHandler
# auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


tweetsonheatmap = config.getint('View', 'tweets on heatmap')
numhotwords = config.getint('View', 'number of hotwords')
numticks = config.getint('View', 'number of ticks in timeline')

stopwords = set([
			'rt', 'today', "didn't", "don't", "[pic]", "i'm", "...", "..", "w/",
			'&amp;',
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