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

import requests
from flask import Flask, request
from pymorphy2 import MorphAnalyzer

from Microservices import Packer, Logger

server = Flask(__name__)
logger = Logger.Logger()
default_port = 5001


class Lemmatizer:
    def __init__(self):
        # Services
        self._morph_analyzer = MorphAnalyzer()

        # Data
        self._stop_words = self._read_stop_words()
        self._parts_of_speech_to_remove = ['NUMR', 'NPRO', 'PREP', 'CONJ']

        logger.info('Lemmatizer was successfully initialized.', __name__)

    @staticmethod
    def _contains_latin_letter(word: str):
        if word:
            return all(map(lambda c: c in ascii_letters, word))

    def _detect_part_of_speech(self, word: str):
        if word:
            return self._morph_analyzer.parse(word)[0].tag.POS

    @staticmethod
    def check_spelling(text):
        default_port = 5004
        data = Packer.pack({'text': text})

        response = requests.get(f'http://localhost:{default_port}/api/spellChecker/checkText',
                                params={'content': data}).content.decode('utf-8')

        return Packer.unpack(response)['response']['text']

    def _is_stop_word(self, word: str):
        if not word:
            logger.warning('Got empty word.', __name__)
            return

        word = f' {word} '

        for stop_words in self._stop_words.values():
            if word in stop_words:
                return True

        return False

    def _remove_words_without_emotions(self, text: str):
        if not text:
            logger.warning('Got empty text.', __name__)
            return

        cleaned_text = list()

        for word in re.findall(r'\w+', text):
            if not self._detect_part_of_speech(word) in self._parts_of_speech_to_remove and \
                    not self._is_stop_word(word):
                cleaned_text.append(word)

        return ' '.join(cleaned_text).strip()

    @staticmethod
    def _find_stop_words():
        wd = os.getcwd()

        while 'Data' not in os.listdir(os.getcwd()):
            os.chdir('..')

        path_to_stop_words = os.path.join(os.getcwd(), 'Data', 'stop_words.json')

        os.chdir(wd)
        return path_to_stop_words

    @staticmethod
    def _read_stop_words():
        path_to_stop_words = Lemmatizer._find_stop_words()

        if os.path.exists(path_to_stop_words):
            with open(path_to_stop_words, 'r', encoding='utf-8') as file:
                return json.load(file)

    def _delete_words_contains_latin_letters(self, text: str):
        text = ' '.join([word for word in re.findall(r'\w+', text.lower())
                         if not self._contains_latin_letter(word) and word.isalpha()]).strip()

        if text:
            return text
        else:
            pass
            logger.warning('All words in document contain latin letters or all words are digits.', __name__)

    def _get_text_normal_form(self, text: str):
        return ' '.join([self._morph_analyzer.parse(word)[0].normal_form + ' ' for word in re.findall(r'\w+', text)]) \
            .strip()

    def get_text_initial_form(self, text):
        if not text:
            logger.warning('Got empty text.', __name__)
            return

        logger.info(f'Start text: {text}', __name__)

        transformations = [self._delete_words_contains_latin_letters, Lemmatizer.check_spelling,
                           self._get_text_normal_form, self._remove_words_without_emotions]

        for transformation in transformations:
            text = transformation(text)

            if not text:
                return

        logger.info(f'Lemmatized text: {text}', __name__)

        return text

    def __del__(self):
        del self._morph_analyzer
        del self._parts_of_speech_to_remove
        del self._stop_words


lemmatizer = Lemmatizer()


@server.route('/api/lemmatizer/getTextInitialForm', methods=['GET'])
def handle():
    logger.info(f'{request.method} request.', __name__)

    response = dict(response=dict(code=400))

    if 'content' in request.args:
        content = Packer.unpack(request.args['content'])
        logger.info(f'Params: {str(content)}', __name__)
    else:
        logger.error('Bad request.', __name__)
        return Packer.pack(response)

    if 'text' in content:
        text = content['text']
    else:
        return Packer.pack(response)

    response['response']['lemmatized_text'] = lemmatizer.get_text_initial_form(text)

    # print(response)
    return Packer.pack(response)


try:
    server.run(port=default_port)
except BaseException as exception:
    logger.fatal(f'Error while trying to start server: {str(exception)}', __name__)
