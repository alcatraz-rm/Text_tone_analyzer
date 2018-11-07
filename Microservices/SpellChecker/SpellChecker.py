import requests
from flask import Flask, request
from Microservices import Packer

# from Python.Services.ExceptionsHandler import ExceptionsHandler
# from Python.Services.Logger import Logger

server = Flask(__name__)
default_port = 5002


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
    response = dict(response=dict(code=400))

    if 'content' in request.args:
        content = Packer.unpack(request.args['content'])
    else:
        return Packer.pack(response)

    if 'text' in content:
        text = content['text']
    else:
        return Packer.pack(response)

    response['response']['text'] = spell_checker.check_spelling(text)
    response['response']['code'] = 200

    return Packer.pack(response)


server.run(debug=True, port=default_port)
