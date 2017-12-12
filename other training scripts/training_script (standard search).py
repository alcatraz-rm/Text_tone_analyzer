import requests


access_token = '2361221932-dsYEXSV10UFUTkKqt2oS0PpUek5o7FaGO4Od1s0'
access_token_secret = 'mQFmIODWdurpz4oVBkdUSi6K8LascxvvTiHa5JZDwlA6a'
consumer_key = '7jK49ES2ZDv0DL6Jsxm9wIdDx'
consumer_key_secret = 'yOLMq677FX0n2MEMarOKaqYEqTXAVaAFRiqIntiRSUyu6fauwT'

response = requests.get('https://api.twitter.com/1.1/search/tweets.json', params={
    'q': 'Сбербанк',
    'result_type': 'mixed',
    'count': 5
})

print(response)
