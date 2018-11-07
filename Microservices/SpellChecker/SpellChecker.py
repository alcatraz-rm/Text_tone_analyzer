import requests

from Microservices.Logger import Logger


# from Python.Services.ExceptionsHandler import ExceptionsHandler
# from Python.Services.Logger import Logger


class SpellChecker:
    def __init__(self):
        pass
        # Services
        self.__logger = Logger()
        # self._exceptions_handler = ExceptionsHandler()

        self.__logger.info('SpellChecker was successfully initialized.', __name__)

    def check_spelling(self, text: str):
        self.__logger.info(f'Start text: {text}', __name__)

        try:
            response = requests.get('https://speller.yandex.net/services/spellservice.json/checkText', params={
                'text': text}).json()

        except BaseException as exception:
            # self.__logger.error(self._exceptions_handler.get_error_message(exception), __name__)
            return text

        for word in response:
            text = text.replace(word['word'], word['s'][0])

        self.__logger.info(f'Checked text: {text}', __name__)
        return text
