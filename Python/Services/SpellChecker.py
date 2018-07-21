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
        self.logger = Logger()

        if not self.logger.configured:
            self.logger.configure()

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
