import ConfigParser
from twitter import OAuth

config = ConfigParser.RawConfigParser()
config.read('keys.cfg')

CONSUMER_KEY = config.get('OAuth', 'API key')
CONSUMER_SECRET = config.get('OAuth', 'API secret')
OAUTH_TOKEN = config.get('OAuth', 'Access token')
OAUTH_TOKEN_SECRET = config.get('OAuth', 'Access token secret')

auth = OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)