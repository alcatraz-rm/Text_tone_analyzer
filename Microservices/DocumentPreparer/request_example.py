import requests
from Microservices import Packer

data = Packer.pack({'text': input('text: ')})

response = requests.get(f'http://localhost:5000/document/split/trigrams',
                        params={'content': data}).content.decode('utf-8')

unigrams = Packer.unpack(response)['response']['trigrams']
print(unigrams)
