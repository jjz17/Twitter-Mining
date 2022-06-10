import tweepy
from utils import auth, api
import json
from pprint import pprint

'''
Get friends
'''
# friends = tweepy.Cursor(api.get_friends).items(30)
# for i, f in enumerate(friends):
#     print(f'{i}. {f.screen_name}, ID: {f.id}')
# print(type(friends))

'''
Data collection and storage
'''
tweet_data = {}
for status in tweepy.Cursor(api.home_timeline).items(30):
    # Process a single status
    user = status.user
    print(user.screen_name)
    if user.screen_name in tweet_data:
        # tweet_data[user.screen_name] = tweet_data[user.screen_name].append(status)
        tweet_data[user.screen_name] += [status._json]
    else:
        tweet_data[user.screen_name] = [status._json]

with open('data.json', 'w') as f:
    # Dump appended data to file
    json.dump(tweet_data, f)
    f.close()

'''
Data collection and storage
'''
# tweet_data = []
# query = 'NBA Finals 2022'
# # for status in tweepy.Cursor(api.home_timeline).items(2):
# for status in tweepy.Cursor(api.search_tweets, q=query, lang='en', result_type='mixed', count=10).items(10):
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
'''
Dict parsing
'''
# query = 'NBA Finals 2022'
# # Create list of dictionaries of tweet data
# tweets = [tweet._json for tweet in tweepy.Cursor(
#     api.search_tweets, q=query, lang='en', result_type='mixed', count=10).items(10)]
# # Parse out useful information from each dict
# '''
# dict_keys(['created_at', 'id', 'id_str', 'text', 'truncated', 'entities', 'metadata', 'source', 'in_reply_to_status_id',
# 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'in_reply_to_screen_name', 'user', 'geo', 
# 'coordinates', 'place', 'contributors', 'is_quote_status', 'retweet_count', 'favorite_count', 'favorited', 'retweeted', 
# 'possibly_sensitive', 'lang'])
# '''
# # simple_tweets = [{k: tweet[k] for k in ['user', 'text', 'geo', 'coordinates',
# #                                         'retweet_count', 'favorite_count']} for tweet in tweets]
# simple_tweets = [{k: tweet[k] for k in ['text']} for tweet in tweets]
                            
# for tw in simple_tweets:
#     pprint(tw)
