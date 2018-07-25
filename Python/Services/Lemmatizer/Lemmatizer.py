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

from string import ascii_letters
import re
import json
import os
import pymorphy2
from Python.Services.SpellChecker import SpellChecker
from Python.Services.Logger import Logger


class Lemmatizer:
    def __init__(self):
        self._spell_checker = SpellChecker()
        self.__logger = Logger()

        if not self.__logger.configured:
            self.__logger.configure()

        self._parts_of_speech = self._read_parts_of_speech()
        self._morph_analyzer = pymorphy2.MorphAnalyzer()

        self.__logger.info('Lemmatizer was successfully initialized.', 'Lemmatizer.__init__()')

    @staticmethod
    def _contains_latin_letter(word):
        return all(map(lambda c: c in ascii_letters, word))

    @staticmethod
    def _read_parts_of_speech():
        if os.getcwd().endswith('Python'):
            parts_of_speech_path = os.path.join('Services', 'Lemmatizer', 'parts_of_speech.json')

        elif os.getcwd().endswith('Tests'):
            parts_of_speech_path = os.path.join('..', 'Services', 'Lemmatizer', 'parts_of_speech.json')

        else:
            parts_of_speech_path = 'parts_of_speech.json'

        with open(parts_of_speech_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def lead_to_initial_form(self, text):
        self.__logger.info('Start text: %s' % text, 'Lemmatizer.lead_to_initial_form()')

        words = re.findall(r'\w+', self._spell_checker.check(text.lower()))

        words = [word for word in words if word.isalpha()
                 and not self._contains_latin_letter(word)]

        words = [self._morph_analyzer.parse(word)[0].normal_form + ' ' for word in words]

        text = ' ' + ''.join(words) + ' '

        for part_of_speech in self._parts_of_speech.values():
            for word in part_of_speech:
                text = text.replace(word, ' ')

        text = text.strip()
        self.__logger.info('Lemmatized text: %s' % text, 'Lemmatizer.lead_to_initial_form()')

        return text
