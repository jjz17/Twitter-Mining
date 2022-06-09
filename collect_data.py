import tweepy
from utils import auth, api
import json


# tweet_data = []
# for status in tweepy.Cursor(api.home_timeline).items(2):
#     # Process a single status
#     tweet_data.append(status._json)

# with open('empty.json', 'r') as f:
#     # Load currently stored json array
#     data = json.load(f)
#     # Append existing data with new data
#     data = data + tweet_data
#     with open('empty.json', 'w') as f2:
#         # Dump appended data to file
#         json.dump(data, f2)
#         f2.close()
#     f.close()

query = 'NBA'
tweets = [tweet._json for tweet in tweepy.Cursor(api.search_tweets, q=query, lang='en', result_type='mixed', count=10).items(1)]
for tweet in tweets:
    print(tweet.keys())