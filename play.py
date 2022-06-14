import json
import pandas as pd

# with open('data.json', 'r') as file:
#     data = json.load(file)
#     for user_tweets in data.values():
#         for tweet in user_tweets:
#             print(tweet['coordinates'])

sentiment_data = pd.read_csv('sentiment.csv').sort_values('User')
# sentiment_data = sentiment_data.query("User == 'NovusOrdoWatch'")
time_data = pd.read_csv('time_tweet.csv')
gb = time_data.groupby(['Time','User','Sentiment']).count()
print(type(gb))
gb.to_csv('test.csv', index=False
)