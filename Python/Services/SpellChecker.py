# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import os
import sys
import requests
sys.path.append(os.path.join('..', '..'))

from Python.Services.Logger import Logger


class SpellChecker:
    def __init__(self):
        self.__logger = Logger()

        if not self.__logger.configured:
            self.__logger.configure()

        self.__logger.info('SpellChecker was successfully initialized.', 'SpellChecker.__init__()')

    def check(self, text):
        self.__logger.info('start text: %s' % text, 'SpellChecker.check()')

        try:
            response = requests.get('https://speller.yandex.net/services/spellservice.json/checkText', params={
                'text': text}).json()

            for word in response:
                text = text.replace(word['word'], word['s'][0])

        except requests.exceptions.ConnectionError or BaseException:
            self.__logger.error('Internet connection error.', 'SpellChecker.check()')
            return text

        self.__logger.info('checked text: %s' % text, 'SpellChecker.check()')
        return text
