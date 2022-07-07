import tweepy
from tweepy import OAuthHandler
from dotenv import load_dotenv
import os

import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from pprint import pprint
from numpy import argmax
import pandas as pd
import pymongo
from pymongo import MongoClient

'''
Tweepy API Setup
'''

load_dotenv()

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_KEY_SECRET = os.getenv('CONSUMER_KEY_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


'''
Sentiment Analysis model and tokenizer
'''

roberta = "cardiffnlp/twitter-roberta-base-sentiment-latest"
model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)


'''
Mongo client and connection
'''
client = MongoClient()
db = client['socialAnalyticsDB']
collection = db['twitter']


'''
Utility functions for collecting/processing data
'''


def get_mongo_data():
    data = []
    for doc in collection.find():
        data.append({'user': doc['user'], 'tweets': doc['tweets']})
    return data


def preprocess_text(text: str) -> str:
    '''
    Preprocess tweet text for the model
    '''
    words = []
    for word in text.split(' '):
        if word.startswith('@') and len(word) > 1:
            word = '@user'
        elif word.startswith('http'):
            word = "http"
        words.append(word)
    return ' '.join(words)


def analyze_sentiment(text):
    labels = ['Negative', 'Neutral', 'Positive']
    processed_text = preprocess_text(text)
    # sentiment analysis
    encoded_tweet = tokenizer(processed_text, return_tensors='pt')
    output = model(**encoded_tweet)

    # Convert output pytorch tensor to numpy array by detaching the computational graph
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    ind = argmax(scores)

    for label, score in zip(labels, scores):
        # print(f'\t{label}: {score}')
        pass

    sentiment = labels[ind]
    return sentiment


def time_to_sent(data: pd.DataFrame) -> pd.DataFrame:
    '''
    Aggregate sentiment counts per user with pivot tables
    data has columns: User, Text, Sentiment, Time
    '''
    data = data.drop(['Text'], axis=1)
    pt = pd.pivot_table(data, values='Time',index='User', columns='Sentiment', aggfunc='count').fillna(0)
    return pt