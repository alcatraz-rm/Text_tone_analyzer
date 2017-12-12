import requests
import time


response = requests.get('https://api.twitter.com/oauth/request_token', headers={
    'oauth_consumer_key': '7jK49ES2ZDv0DL6Jsxm9wIdDx',
    'oauth_signature_method': 'HMAC-SHA1',
    'oauth_version': '1.0',
    'oauth_nonce': 'K7ny27JTpKVsTgdyLdDfmQQWVLERj2zAK5BslRsqyw',
    'oauth_signature': 'Pc%2BMLdv028fxCErFyi8KXFM%2BddU%3D'
})

print(response)
