import requests
from Microservices import Packer

data = Packer.pack({'text': input('text: ')})
default_port = 5002

response = requests.get(f'http://localhost:{default_port}/spellChecker/checkText',
                        params={'content': data}).content.decode('utf-8')

checked_text = Packer.unpack(response)['response']['text']

print(checked_text)
