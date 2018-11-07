import requests
from flask import Flask, request

from Python.Services.ExceptionsHandler import ExceptionsHandler
from Python.Services.Logger import Logger

server = Flask(__name__)


class SpellChecker:
    def __init__(self):
        pass
        # Services
        # self.__logger = Logger()
        # self._exceptions_handler = ExceptionsHandler()

        # self.__logger.info('SpellChecker was successfully initialized.', __name__)

    def check_spelling(self, text: str):
        # self.__logger.info(f'Start text: {text}', __name__)

        try:
            response = requests.get('https://speller.yandex.net/services/spellservice.json/checkText', params={
                'text': text}).json()

        except BaseException as exception:
            # self.__logger.error(self._exceptions_handler.get_error_message(exception), __name__)
            return text

        for word in response:
            text = text.replace(word['word'], word['s'][0])

        # self.__logger.info(f'Checked text: {text}', __name__)
        return text

spell_checker = SpellChecker()


@server.route('/spellChecker/checkText', methods=['GET'])
def request_handle():
    if 'text' in request.args:
        text = ''.join([str(chr(int(code))) for code in request.args['text'].split(',')])
    else:
        return None, 400

    text = spell_checker.check_spelling(text)

    return ','.join([str(ord(char)) for char in text])


server.run(debug=True)
