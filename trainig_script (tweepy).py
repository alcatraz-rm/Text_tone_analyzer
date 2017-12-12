import tweepy
import requests
from pprint import pprint
import chardet


def twitter_api_init():
    access_token = '2361221932-dsYEXSV10UFUTkKqt2oS0PpUek5o7FaGO4Od1s0'
    access_token_secret = 'mQFmIODWdurpz4oVBkdUSi6K8LascxvvTiHa5JZDwlA6a'
    consumer_key = 'BIOnPOxlvyCYo5BSZECv91Aqe'
    consumer_key_secret = 'Lm6h7xq8THuOogrIOaOLZU3azq5DfNJkcV3Fl5u9R5SmJJl9ec'

    auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)


api = twitter_api_init()
tweets = []
tweepy_cursor = tweepy.Cursor(api.search, q='Сбербанк', count=100)

with open('test.txt', 'w') as file:
    for num, tweet in enumerate(tweepy_cursor.items()):
        act = input()
        if act == 'q':
            break

        try:
            text = tweet.text
            print(str(num) + ': ' + text)
            file.write(text)
            tweets.append(text)
        except:
            print('err')
        # except:
        #     break

        # if num == 100:
        #     break


with open('test.txt', 'rb') as file:
    s = file.read()
    encoding = chardet.detect(s)['encoding']
    print(encoding)
    s = s.decode(encoding)
    print(s)

with open('test.txt', 'r') as file:
    s = file.read()

with open('test.txt', 'w', encoding=encoding) as file:
     s = s.encode('utf-8').decode(encoding)
     file.write(s)

# pprint(tweets)
