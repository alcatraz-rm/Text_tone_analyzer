import requests


class SpellChecker:
    def __init__(self):
        pass

    def check(self, text):
        try:
            response = requests.get('https://speller.yandex.net/services/spellservice.json/checkText', params={
                'text': text}).json()

            for word in response:
                text = text.replace(word['word'], word['s'][0])

        except requests.exceptions.ConnectionError:
            return text

        except BaseException:
            return text

        return text
