import requests


response = bytes(requests.get('http://localhost:5000/hello').content).decode('utf-8')
print(response)
