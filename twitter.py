from twitter import *

# MY_TWITTER_CREDS = os.path.expanduser('./.twitter_api_credentials')
# if not os.path.exists(MY_TWITTER_CREDS):
#     oauth_dance("My App Name", CONSUMER_KEY, CONSUMER_SECRET,
#                 MY_TWITTER_CREDS)

# oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

# twitter = Twitter(auth=OAuth(
#     '1673455951-jdJJJEtQJl4tCJEu0SvlWWv6XMEQ8BmEypFdUBH', 'JJyDgffBQwvKl2GfwowL8xnqZqY9Sw9WeSRTOGlk679LS', 'yiVNsD8FzcsruSBpdDpRAfoqx', 'JW4lBqpUQI2BXKDl1xc01YKBCRiDWW2IlDsZ1t6pKsiHHyACBY'))


auth = OAuth(
    token='1673455951-jdJJJEtQJl4tCJEu0SvlWWv6XMEQ8BmEypFdUBH',
    token_secret='JJyDgffBQwvKl2GfwowL8xnqZqY9Sw9WeSRTOGlk679LS',
    consumer_key='yiVNsD8FzcsruSBpdDpRAfoqx',
    consumer_secret='JW4lBqpUQI2BXKDl1xc01YKBCRiDWW2IlDsZ1t6pKsiHHyACBY'
)

# stream status
twitter_stream = TwitterStream(auth=auth)
iterator = twitter_stream.statuses.sample()

for tweet in iterator:
    # ...do something with this tweet...


# Search for the latest tweets about query, #tag
# t.search.tweets(q="#pycon")
t = Twitter(auth=auth)
t.search.tweets(q="snow")