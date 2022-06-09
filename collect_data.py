import tweepy
from utils import auth, api
import json


tweet_data = []
for status in tweepy.Cursor(api.home_timeline).items(2):
    # Process a single status
    tweet_data.append(status._json)

with open('empty.json', 'r') as f:
    # Load currently stored json array
    data = json.load(f)
    # Append existing data with new data
    data = data + tweet_data
    with open('empty.json', 'w') as f2:
        # Dump appended data to file
        json.dump(data, f2)
        f2.close()
    f.close()

# with open('empty.json', 'r+') as f:
#     data = json.load(f)
#     # If json file was empty
#     if not data:
#         data = data + tweet_data
#         # Delete original contents
#         f.truncate()
#         with open('empty.json', 'w') as f2:
#             json.dump(data, f2)
#         f.close()

# for status in tweepy.Cursor(api.home_timeline).items(10):
#     # Process a single status
#     print(status._json)