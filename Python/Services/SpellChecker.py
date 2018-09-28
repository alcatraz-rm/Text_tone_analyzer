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


class SpellChecker:
    def __init__(self):
        self.__logger = Logger()

        self.__logger.info('SpellChecker was successfully initialized.', 'SpellChecker.__init__()')

    def check_spelling(self, text):
        self.__logger.info(f'Start text: {text}', 'SpellChecker.check_spelling()')

        try:
            response = requests.get('https://speller.yandex.net/services/spellservice.json/checkText', params={
                'text': text}).json()

            for word in response:
                text = text.replace(word['word'], word['s'][0])

        except requests.exceptions.ConnectionError or BaseException:
            self.__logger.error('Internet connection error.', 'SpellChecker.check_spelling()')
            return text

        self.__logger.info(f'Checked text: {text}', 'SpellChecker.check_spelling()')
        return text
