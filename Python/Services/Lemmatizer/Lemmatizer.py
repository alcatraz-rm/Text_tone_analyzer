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

import os
from string import ascii_letters
import re
import json
import pymorphy2
from Python.Services.SpellChecker import SpellChecker
from Python.Services.Logger import Logger
from Python.Services.PathService import PathService


class Lemmatizer:
    def __init__(self):
        self._spell_checker = SpellChecker()
        self.__logger = Logger()
        self._path_service = PathService()

        self._parts_of_speech = self._read_parts_of_speech()
        self._morph_analyzer = pymorphy2.MorphAnalyzer()

        self._parts_of_speech_to_remove = ['NUMR', 'NPRO', 'PREP']

        self.__logger.info('Lemmatizer was successfully initialized.', 'Lemmatizer.__init__()')

    @staticmethod
    def _contains_latin_letter(word):
        if word:
            return all(map(lambda c: c in ascii_letters, word))

    def _detect_part_of_speech(self, word):
        if word:
            return self._morph_analyzer.parse(word)[0].tag.POS

    def _word_in_parts_of_speech_list(self, word):
        if not word:
            self.__logger.warning('Got empty word.', 'Lemmatizer._word_in_parts_of_speech_list()')
            return

        word = word.join([' ', ' '])

        for part_of_speech in self._parts_of_speech.values():
            if word in part_of_speech:
                return True

        return False

    def _remove_words_without_emotions(self, text):
        if not text:
            self.__logger.warning('Got empty text.', 'Lemmatizer._remove_word_without_emotions()')
            return

        cleaned_text = list()

        for word in re.findall(r'\w+', text):
            if not self._detect_part_of_speech(word) in self._parts_of_speech_to_remove and \
                    not self._word_in_parts_of_speech_list(word):

                cleaned_text.append(word)

        return ' '.join(cleaned_text).strip()

    def _read_parts_of_speech(self):
        if os.path.exists(self._path_service.path_to_parts_of_speech):
            with open(self._path_service.path_to_parts_of_speech, 'r', encoding='utf-8') as file:
                return json.load(file)

    def _delete_words_contains_latin_letters(self, text):
        text = ' '.join([word for word in re.findall(r'\w+', self._spell_checker.check_spelling(text.lower()))
                         if not self._contains_latin_letter(word) and word.isalpha()]).strip()

        if text:
            return text
        else:
            self.__logger.warning('All words in document contain latin letters or all words are digits.',
                                  'Lemmatizer.lead_to_initial_form()')

    def _get_words_normal_form(self, text):
        return ' '.join([self._morph_analyzer.parse(word)[0].normal_form + ' ' for word in re.findall(r'\w+', text)])\
                                                                                                            .strip()

    def lead_to_initial_form(self, text):
        if not text:
            self.__logger.warning('Got empty text.', 'Lemmatizer.lead_to_initial_form()')
            return

        self.__logger.info(f'Start text: {text}', 'Lemmatizer.lead_to_initial_form()')

        actions = [self._delete_words_contains_latin_letters, self._get_words_normal_form,
                   self._remove_words_without_emotions]

        for action in actions:
            text = action(text)

            if not text:
                return

        self.__logger.info(f'Lemmatized text: {text}', 'Lemmatizer.lead_to_initial_form()')
        return text
