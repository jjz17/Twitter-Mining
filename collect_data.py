import tweepy
from utils import auth, api

for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    print(status.text)

# for status in tweepy.Cursor(api.home_timeline).items(10):
#     # Process a single status
#     print(status._json)
