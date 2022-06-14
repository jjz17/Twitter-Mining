import json

# with open('data.json', 'r') as file:
#     data = json.load(file)
#     for user_tweets in data.values():
#         for tweet in user_tweets:
#             print(tweet['coordinates'])

# with open('test.json', 'r') as infile, open('test.json', 'w') as outfile:
#     try:
#         data = json.load(infile)
#         print(data)
#         l = [1,2,3]
#         for item in l:
#             data[item] = item
#         print(data)
#         json.dump(data, outfile)
#         infile.close()
#         outfile.close()
#     except json.JSONDecodeError:
#         print('Error decoding JSON')
#         data = {}
#         l = [4,5,6]
#         for item in l:
#             data[item] = item
#         json.dump(data, outfile)
#         infile.close()
#         outfile.close()


with open('test.json', 'r') as infile:
    try:
        data = json.load(infile)
        print(data)
        l = [1,2,3]
        for item in l:
            if str(item) in data:
                pass
            else:
                data[item] = item
        print(data)
        with open('test.json', 'w') as outfile:
            json.dump(data, outfile)
            infile.close()
            outfile.close()
    except:
        data = {}
        l = [4,5,6]
        for item in l:
            data[item] = item
        print(data)
        with open('test.json', 'w') as outfile:
            json.dump(data, outfile)
            infile.close()
            outfile.close()
