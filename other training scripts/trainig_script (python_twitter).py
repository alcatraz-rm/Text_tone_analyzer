import twitter
from pprint import pprint


def twitter_api_init():
    access_token = '2361221932-dsYEXSV10UFUTkKqt2oS0PpUek5o7FaGO4Od1s0'
    access_token_secret = 'mQFmIODWdurpz4oVBkdUSi6K8LascxvvTiHa5JZDwlA6a'
    consumer_key = 'BIOnPOxlvyCYo5BSZECv91Aqe'
    consumer_key_secret = 'Lm6h7xq8THuOogrIOaOLZU3azq5DfNJkcV3Fl5u9R5SmJJl9ec'

    api = twitter.OAuth(consumer_key=consumer_key,
                      consumer_secret=consumer_key_secret, token=access_token, token_secret=access_token_secret)

    return api


api = twitter_api_init()
print(dir(twitter.api.Twitter))
