import tweepy
from pprint import pprint
import json
import copy
import chardet


def twitter_auth():
    consumer_key = '7jK49ES2ZDv0DL6Jsxm9wIdDx'
    consumer_secret = 'yOLMq677FX0n2MEMarOKaqYEqTXAVaAFRiqIntiRSUyu6fauwT'
    access_token = '2361221932-dsYEXSV10UFUTkKqt2oS0PpUek5o7FaGO4Od1s0'
    access_token_secret = 'mQFmIODWdurpz4oVBkdUSi6K8LascxvvTiHa5JZDwlA6a'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)


def parse(result):
    tmp_positive = []
    tmp_negative = []
    # tmp = {'text': text}
    tmp = dict()
    for tweet in result:
        if len(tweet.text) < 139:
            tmp_text = tweet.text
            print(tmp_text)
            tmp['text'] = tmp_text
            tonal = input('Tonal: ')  # 'p'/'n'/'s'

            if tonal.strip().lower() == 'p':
                tmp_positive.append(tmp)
                tmp_positive = copy.deepcopy(tmp_positive)
            elif tonal.strip().lower() == 'n':
                tmp_negative.append(tmp)
                tmp_negative = copy.deepcopy(tmp_negative)
            elif tonal.strip().lower() == 'stop':
                break

    return tmp_positive, tmp_negative


api = twitter_auth()
tmp_positive = []
tmp_negative = []
search_text = '1'
search_text_prev = ''

while search_text:
    search_text = input('Query: ')

    if search_text.strip().lower() == 'stop':
        break

    while not search_text:
        search_text = input('Query: ')

    if 'prev' in search_text.strip().lower():
        search_text = search_text_prev

    result = api.search(q=search_text)
    tmp = parse(result)
    tmp_positive.extend(tmp[0])
    tmp_negative.extend(tmp[1])
    search_text_prev = search_text


positive = {'results': tmp_positive}
negative = {'results': tmp_negative}
with open('positive.json', 'w') as file:
    json.dump(positive, file, indent=4)

with open('negative.json', 'w') as file:
    json.dump(negative, file, indent=4)

with open('positive.txt', 'w', encoding='utf-8') as file:
    file.write(json.dumps(positive, indent=4))

with open('negative.txt', 'w', encoding='utf-8') as file:
    file.write(json.dumps(negative, indent=4))

with open('negative.txt', 'rb') as file:
    encoding = chardet.detect(file.read())['encoding']
    print(encoding)

with open('positive.txt', 'r', encoding='utf-8') as file:
    positive_read = json.loads(file.read())

with open('negative.txt', 'r', encoding='utf-8') as file:
    negative_read = json.loads(file.read())

pprint(positive_read)
pprint(negative_read)
