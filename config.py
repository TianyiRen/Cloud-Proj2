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