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

import json
import os
import re
from string import ascii_letters

import pymorphy2

from Python.Services.Logger import Logger
from Python.Services.PathService import PathService
from Python.Services.SpellChecker import SpellChecker


class Lemmatizer:
    def __init__(self):
        # Services
        self._spell_checker = SpellChecker()
        self.__logger = Logger()
        self._path_service = PathService()
        self._morph_analyzer = pymorphy2.MorphAnalyzer()

        # Data
        self._stop_words = self._read_stop_words()
        self._parts_of_speech_to_remove = ['NUMR', 'NPRO', 'PREP', 'CONJ']

        self.__logger.info('Lemmatizer was successfully initialized.', __name__)

    @staticmethod
    def _contains_latin_letter(word: str):
        if word:
            return all(map(lambda c: c in ascii_letters, word))

    def _detect_part_of_speech(self, word: str):
        if word:
            return self._morph_analyzer.parse(word)[0].tag.POS

    def _is_stop_word(self, word: str):
        if not word:
            self.__logger.warning('Got empty word.', __name__)
            return

        word = f' {word} '

        for stop_words in self._stop_words.values():
            if word in stop_words:
                return True

        return False

    def _remove_words_without_emotions(self, text: str):
        if not text:
            self.__logger.warning('Got empty text.', __name__)
            return

        cleaned_text = list()

        for word in re.findall(r'\w+', text):
            if not self._detect_part_of_speech(word) in self._parts_of_speech_to_remove and\
                    not self._is_stop_word(word):
                cleaned_text.append(word)

        return ' '.join(cleaned_text).strip()

    def _read_stop_words(self):
        if os.path.exists(self._path_service.path_to_stop_words):
            with open(self._path_service.path_to_stop_words, 'r', encoding='utf-8') as file:
                return json.load(file)

    def _delete_words_contains_latin_letters(self, text: str):
        # checked_text = self._spell_checker.check_spelling(text.lower())
        text = ' '.join([word for word in re.findall(r'\w+', text)
                         if not self._contains_latin_letter(word) and word.isalpha()]).strip()

        if text:
            return text
        else:
            self.__logger.warning('All words in document contain latin letters or all words are digits.', __name__)

    def _get_text_normal_form(self, text: str):
        return ' '.join([self._morph_analyzer.parse(word)[0].normal_form + ' ' for word in re.findall(r'\w+', text)]) \
            .strip()

    def get_text_initial_form(self, text: str):
        if not text:
            self.__logger.warning('Got empty text.', __name__)
            return

        self.__logger.info(f'Start text: {text}', __name__)

        transformations = [self._delete_words_contains_latin_letters, self._get_text_normal_form,
                           self._remove_words_without_emotions]

        for transformation in transformations:
            text = transformation(text)

            if not text:
                return

        self.__logger.info(f'Lemmatized text: {text}', __name__)
        return text

    def __del__(self):
        del self._stop_words
        del self._parts_of_speech_to_remove
        del self._morph_analyzer
        del self._path_service
        del self._spell_checker
        del self.__logger
