import requests
from Microservices import Packer

data = Packer.pack({'text': input('text: ')})
default_port = 5001

response = requests.get(f'http://localhost:{default_port}/lemmatizer/getTextInitialForm',
                        params={'content': data}).content.decode('utf-8')

lemmatized_text = Packer.unpack(response)['response']['lemmatized_text']

print(lemmatized_text)
