import requests
import json

text = ','.join([str(ord(char)) for char in list(input('text: '))])

response = requests.get(f'http://localhost:5000/document/split/unigrams', params={'text': text}).content.decode('utf-8')
unigrams = json.loads(''.join([str(chr(int(code))) for code in response.split(',')]),
                      encoding='utf-8')['response']['unigrams']
print(unigrams)
