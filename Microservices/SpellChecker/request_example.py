import requests

text = ','.join([str(ord(char)) for char in list(input('text: '))])

response = requests.get(f'http://localhost:5000/spellChecker/checkText', params={'text': text}).content.decode('utf-8')

checked_text = ''.join([str(chr(int(code))) for code in response.split(',')])

print(checked_text)
