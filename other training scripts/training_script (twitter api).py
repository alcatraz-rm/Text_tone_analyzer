import requests


response = requests.get('https://api.twitter.com/1.1/tweets/search/30day/german_yakimov.json', params={
    'query': 'Сбербанк',
    'maxResults': 10,
    'Authorization': '2361221932-dsYEXSV10UFUTkKqt2oS0PpUek5o7FaGO4Od1s0'
}
)

print(response)
