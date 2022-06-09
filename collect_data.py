import tweepy
from utils import auth, api
import json
from pprint import pprint


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
# Create list of dictionaries of tweet data
tweets = [tweet._json for tweet in tweepy.Cursor(
    api.search_tweets, q=query, lang='en', result_type='mixed', count=10).items(1)]
# Parse out useful information from each dict
'''
dict_keys(['created_at', 'id', 'id_str', 'text', 'truncated', 'entities', 'metadata', 'source', 'in_reply_to_status_id',
'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'in_reply_to_screen_name', 'user', 'geo', 
'coordinates', 'place', 'contributors', 'is_quote_status', 'retweet_count', 'favorite_count', 'favorited', 'retweeted', 
'possibly_sensitive', 'lang'])
'''
simple_tweets = [{k: tweet[k] for k in ['user', 'text', 'geo', 'coordinates',
                                        'retweet_count', 'favorite_count']} for tweet in tweets]
                            
for tw in simple_tweets:
    pprint(tw)
