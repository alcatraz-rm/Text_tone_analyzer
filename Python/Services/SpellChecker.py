# Copyright © 2018. All rights reserved.
# Author: German Yakimov

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests

from Python.Services.Logger import Logger
from Python.Services.ExceptionsHandler import ExceptionsHandler


# TODO: refactor this

class SpellChecker:
    def __init__(self):
        self.__logger = Logger()
        self._exceptions_handler = ExceptionsHandler()

        self.__logger.info('SpellChecker was successfully initialized.', __name__)

    def check_spelling(self, text):
        self.__logger.info(f'Start text: {text}', __name__)

        try:
            response = requests.get('https://speller.yandex.net/services/spellservice.json/checkText', params={
                'text': text}).json()

            for word in response:
                text = text.replace(word['word'], word['s'][0])

        except BaseException as exception:
            self.__logger.error(self._exceptions_handler.get_error_message(exception), __name__)
            return text

        self.__logger.info(f'Checked text: {text}', __name__)
        return text
