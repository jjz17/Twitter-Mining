import pandas as pd
import pymongo
from pymongo import MongoClient
import json
import tweepy
from utils import auth, api, client, db, collection, preprocess_text, analyze_sentiment, get_mongo_data

'''
Ingest data from Tweepy API

Retrieve last 100 tweets on personal home timeline and insert to MongoDB
'''
tweets = tweepy.Cursor(api.home_timeline).items(100)

for i, status in enumerate(tweets):
    user = status.user
    print(f'{i}. {user.screen_name}')
    tweet = status._json
    tweet['sentiment'] = analyze_sentiment(preprocess_text(tweet['text']))
    # Update mongoDB with new tweets
    collection.update_one({'user': user.screen_name},
                          {'$push': {'tweets': tweet}}, upsert=True)


'''
Generate summary statistics csv files from whole mongo DB
'''

data = get_mongo_data()

sent_csv = pd.DataFrame(columns=['User', 'Negative', 'Neutral', 'Positive'])
time_csv = pd.DataFrame(columns=['User', 'Text', 'Sentiment', 'Time'])
for doc in data:
    print('working...')
    user = doc['user']
    tweets = doc['tweets']
    # Process sentiment data
    neg, neu, pos = 0, 0, 0
    for tweet in tweets:
        sentiment = tweet['sentiment']
        if sentiment == 'Negative':
            neg += 1
        elif sentiment == 'Neutral':
            neu += 1
        else:
            pos += 1

        # Process time data
        time = tweet['created_at'].split()
        parsed_time = ' '.join([time[0], time[1], time[2], time[5]])
        row = pd.DataFrame([{'User': user, 'Text': tweet['text'],
                            'Sentiment': tweet['sentiment'], 'Time': parsed_time}])
        time_csv = pd.concat([time_csv, row], ignore_index=True)

    row = pd.DataFrame([{'User': user, 'Negative': neg,
                             'Neutral': neu, 'Positive': pos}])
    sent_csv = pd.concat([sent_csv, row], ignore_index=True)

print(sent_csv)
# Export aggregate sentiment count csv
sent_csv.to_csv('sentiment.csv', index=False)
time_csv.to_csv('time_tweet.csv', index=False)