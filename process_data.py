import json
from textwrap import indent
from nltk.tokenize import word_tokenize
from collections import Counter
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from pprint import pprint
from numpy import argmax
import dash
from dash import dcc
from dash import html
import pandas as pd

 
'''
Example
'''
# with open('empty.json', 'r') as f:
#     counter = Counter()
#     tweets = json.load(f) # load it as a list of Python dicts
#     for tweet in tweets:
#         # Create a list with all the terms
#         terms_all = [term for term in word_tokenize(tweet['text'])]
#         # Update the counter
#         counter.update(terms_all)
#     # Print the first 5 most frequent words
#     print(counter.most_common(5))
#     # print(json.dumps(tweet, indent=4)) # pretty-print
#     # print(type(tweets[0]), len(tweets))

# with open('data.json', 'r') as f:
#     data = json.load(f)
#     for user, tweets in data.items():
#         print(f'User: {user}')
#         for tweet in tweets:
#             print(f'Tweet: {tweet["text"]}')

def get_text_data():
    '''
    Extract tweet texts
    '''
    with open('data.json', 'r') as f:
        data = json.load(f)
        simple_data = {}
        for user, tweets in data.items():
            simple_data[user] = [tweet['text'] for tweet in tweets]
    return(simple_data)


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


def main():
    # Load model and tokenizer
    roberta = "cardiffnlp/twitter-roberta-base-sentiment"

    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)

    labels = ['Negative', 'Neutral', 'Positive']

    csv = pd.DataFrame(columns=['User', 'Negative', 'Neutral', 'Positive'])

    data = get_text_data()
    for user, tweets in data.items():
        print(f'User: {user}')
        neg, neu, pos = 0,0,0
        for tweet in tweets:
            print(f'Tweet: {tweet}')
            processed_text = preprocess_text(tweet)

            # sentiment analysis
            encoded_tweet = tokenizer(processed_text, return_tensors='pt')
            # output = model(encoded_tweet['input_ids'], encoded_tweet['attention_mask'])
            output = model(**encoded_tweet)

            # Convert output pytorch tensor to numpy array by detaching the computational graph
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
            ind = argmax(scores)

            for label, score in zip(labels, scores):
                print(f'\t{label}: {score}')

            classification = labels[ind]
            print(f'Classification: {classification}')
            if classification == 'Negative':
                neg += 1
            elif classification == 'Neutral':
                neu += 1
            else:
                pos += 1
        row = pd.Series({'User': user, 'Negative': neg, 'Neutral': neu, 'Positive': pos})
        # csv = pd.concat([csv, row], ignore_index=True)
        csv = csv.append(row, ignore_index=True)
    print(csv)
    csv.to_csv('sentiment.csv', index=False)


if __name__ == '__main__':
    main()