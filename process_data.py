import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from pprint import pprint
from numpy import argmax
import pandas as pd


def get_data_dict(file_path):
    '''
    Returns the collected Tweet json data as a dict
    '''
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def get_text_data(file_path):
    '''
    Extract tweet texts
    '''
    data = get_data_dict(file_path)
    simple_data = {}
    for user, tweets in data.items():
        simple_data[user] = [tweet['text'] for tweet in tweets]
    return simple_data


def dump_data_dict(data_dict, file_path):
    '''
    Dumps the dict as a json file
    '''
    with open(file_path, 'w') as file:
        json.dump(data_dict, file)
        file.close()


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


def analyze_sentiment(file_path):
    # Load model and tokenizer
    roberta = "cardiffnlp/twitter-roberta-base-sentiment-latest"

    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)

    labels = ['Negative', 'Neutral', 'Positive']

    csv = pd.DataFrame(columns=['User', 'Negative', 'Neutral', 'Positive'])

    # data = get_text_data(file_path)
    data = get_data_dict(file_path)
    for user, tweets in data.items():
        # print(f'User: {user}')
        print('working...')
        neg, neu, pos = 0, 0, 0
        for tweet in tweets:


            '''
            Check if tweet has already been assigned sentiment classification
            '''



            # print(f'Tweet: {tweet["text"]}')
            processed_text = preprocess_text(tweet['text'])

            # sentiment analysis
            encoded_tweet = tokenizer(processed_text, return_tensors='pt')
            # output = model(encoded_tweet['input_ids'], encoded_tweet['attention_mask'])
            output = model(**encoded_tweet)

            # Convert output pytorch tensor to numpy array by detaching the computational graph
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
            ind = argmax(scores)

            for label, score in zip(labels, scores):
                # print(f'\t{label}: {score}')
                pass

            classification = labels[ind]
            # print(f'Classification: {classification}')
            if classification == 'Negative':
                neg += 1
            elif classification == 'Neutral':
                neu += 1
            else:
                pos += 1
            tweet['sentiment'] = classification
        row = pd.DataFrame([{'User': user, 'Negative': neg,
                             'Neutral': neu, 'Positive': pos}])
        csv = pd.concat([csv, row], ignore_index=True)
        # csv = csv.append(row, ignore_index=True)
    print(csv)
    csv.to_csv('sentiment.csv', index=False)
    dump_data_dict(data, file_path)


def generate_timestamp_csv(file_path):
    data = get_data_dict(file_path)
    csv = pd.DataFrame(columns=['User', 'Text', 'Sentiment', 'Time'])
    for user, tweets in data.items():
        for tweet in tweets:
            time = tweet['created_at'].split()
            parsed_time = ' '.join([time[0], time[1], time[2], time[5]])
            row = pd.DataFrame([{'User': user, 'Text': tweet['text'],
                        'Sentiment': tweet['sentiment'], 'Time': parsed_time}])
            csv = pd.concat([csv, row], ignore_index=True)
    csv.to_csv('time_tweet.csv', index=False)


if __name__ == '__main__':
    analyze_sentiment('data.json')
    generate_timestamp_csv('data.json')
