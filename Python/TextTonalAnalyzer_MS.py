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

import json
import os
from subprocess import Popen
import sys


class Packer:
    @staticmethod
    def pack(data):
        return ','.join([str(ord(char)) for char in list(json.dumps(data, ensure_ascii=True))])

    @staticmethod
    def unpack(data):
        return json.loads(''.join([str(chr(int(code))) for code in data.split(',')]), encoding='utf-8')


def _find_server_script():
    wd = os.getcwd()

    while 'Microservices' not in os.listdir(os.getcwd()):
        os.chdir('..')

    path_to_ms = os.path.join(os.getcwd(), 'Microservices')
    os.chdir(wd)

    return os.path.join(path_to_ms, 'ApiGateway.py')


def _start_server():
        path_to_script = _find_server_script()

        Popen([sys.executable, path_to_script])


class TextTonalAnalyzer:
    def __init__(self, classifier_name=None):
        # system configuration
        self._api_gateway_port = 5004
        self._request_url_template = f'http://localhost:{self._api_gateway_port}/api/'

        _start_server()

    def _prepare_text(self, text):
        lemmatizer_response = requests.get(
            f'{self._request_url_template}lemmatizer/getTextInitialForm',
            params={'content': Packer.pack({'text': text})}).content.decode('utf-8')

        lemmatized_text = Packer.unpack(lemmatizer_response)['response']['lemmatized_text']

        splitter_response = requests.get(f'{self._request_url_template}document/split_unigrams',
                                         params={
                                                    'content': Packer.pack({'text': lemmatized_text})
                                                }).content.decode('utf-8')

        unigrams = Packer.unpack(splitter_response)['response']['unigrams']

        splitter_response = requests.get(f'{self._request_url_template}document/split_bigrams',
                                         params={
                                                    'content': Packer.pack({'text': lemmatized_text})
                                         }).content.decode('utf-8')

        bigrams = Packer.unpack(splitter_response)['response']['bigrams']

        splitter_response = requests.get(f'{self._request_url_template}document/split_trigrams',
                                         params={
                                                    'content': Packer.pack({'text': lemmatized_text})
                                         }).content.decode('utf-8')

        trigrams = Packer.unpack(splitter_response)['response']['trigrams']

        return unigrams, bigrams, trigrams

    def _extract_features(self, unigrams, bigrams=None, trigrams=None):
        unigrams_response = requests.get(f'{self._request_url_template}featureExtraction/unigramsWeight',
                                         params={
                                             'content': Packer.pack({'unigrams': unigrams})
                                         }).content.decode('utf-8')

        response = Packer.unpack(unigrams_response)['response']

        if response['code'] == 200:
            unigrams_weight = response['unigrams_weight']
        else:
            return None, None, None

        bigrams_response = requests.get(f'{self._request_url_template}featureExtraction/bigramsWeight',
                                        params={
                                            'content': Packer.pack({'bigrams': bigrams})
                                        }).content.decode('utf-8')

        response = Packer.unpack(bigrams_response)['response']

        if response['code'] == 200:
            bigrams_weight = response['bigrams_weight']
        else:
            return unigrams_weight, None, None

        trigrams_response = requests.get(f'{self._request_url_template}featureExtraction/trigramsWeight',
                                         params={
                                             'content': Packer.pack({'trigrams': trigrams})
                                         }).content.decode('utf-8')

        response = Packer.unpack(trigrams_response)['response']

        if response['code'] == 200:
            trigrams_weight = response['trigrams_weight']
        else:
            return unigrams_weight, bigrams_weight, None

        return unigrams_weight, bigrams_weight, trigrams_weight

    def _predict_tonal(self, unigrams_weight, bigrams_weight=None, trigrams_weight=None):
        unigrams_weight = unigrams_weight or 0
        bigrams_weight = bigrams_weight or 0
        trigrams_weight = trigrams_weight or 0

        response = requests.get(f'{self._request_url_template}classifier/predict',
                                params={'content':
                                        Packer.pack({'unigrams_weight': str(unigrams_weight),
                                                     'bigrams_weight': str(bigrams_weight),
                                                     'trigrams_weight': str(trigrams_weight)})}).content.decode('utf-8')

        response = Packer.unpack(response)

        # print(response)
        return response['response']['tonal'], response['response']['probability']

    def detect_tonal(self, text):
        unigrams, bigrams, trigrams = self._prepare_text(text)

        unigrams_weight, bigrams_weight, trigrams_weight = self._extract_features(unigrams, bigrams, trigrams)

        return self._predict_tonal(unigrams_weight, bigrams_weight, trigrams_weight)
