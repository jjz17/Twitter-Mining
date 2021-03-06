import tweepy
from utils import auth, api
import json
import pymongo
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime

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
# tweet_data = {}
# for i, status in enumerate(tweepy.Cursor(api.home_timeline).items(100)):
#     # Process a single status
#     user = status.user
#     print(f'{i}. {user.screen_name}')
#     if user.screen_name in tweet_data:
#         # tweet_data[user.screen_name] = tweet_data[user.screen_name].append(status)
#         tweet_data[user.screen_name] += [status._json]
#     else:
#         tweet_data[user.screen_name] = [status._json]

# with open(f'data{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.json', 'w') as file:
#     # Dump appended data to file
#     json.dump(tweet_data, file)
#     file.close()


'''
Retrieve last 100 tweets on personal home timeline
'''
# tweets = tweepy.Cursor(api.home_timeline).items(100)
# with open('data.json', 'r') as infile:
#     try:
#         data = json.load(infile)
#     except:
#         data = {}

#     for i, status in enumerate(tweets):
#         user = status.user
#         print(f'{i}. {user.screen_name}')
#         if user.screen_name in data:
#             data[user.screen_name] += [status._json]
#         else:
#             data[user.screen_name] = [status._json]
#     with open('data.json', 'w') as outfile:
#         json.dump(data, outfile)
#         infile.close()
#         outfile.close()


'''
Retrieve last 100 tweets on personal home timeline and insert to MongoDB
'''
tweets = tweepy.Cursor(api.home_timeline).items(100)

client = MongoClient()
db = client['socialAnalyticsDB']
collection = db['twitter']

for i, status in enumerate(tweets):
    user = status.user
    print(f'{i}. {user.screen_name}')
    collection.update_one({'user': user.screen_name},
                          {'$push': {'tweets': status._json}}, upsert=True)

client.close()


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
