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
from Microservices import Packer


def prepare_text(text):
    default_gateway_port = 5004

    lemmatizer_response = requests.get(f'http://localhost:{default_gateway_port}/api/lemmatizer/getTextInitialForm',
                                       params={'content':
                                               Packer.pack({'text': text})}).content.decode('utf-8')
    lemmatized_text = Packer.unpack(lemmatizer_response)['response']['lemmatized_text']

    splitter_response = requests.get(f'http://localhost:{default_gateway_port}/api/document/split_unigrams',
                                     params={'content':
                                             Packer.pack({'text': lemmatized_text})}).content.decode('utf-8')
    unigrams = Packer.unpack(splitter_response)['response']['unigrams']

    splitter_response = requests.get(f'http://localhost:{default_gateway_port}/api/document/split_bigrams',
                                     params={'content':
                                             Packer.pack({'text': lemmatized_text})}).content.decode('utf-8')
    bigrams = Packer.unpack(splitter_response)['response']['bigrams']

    splitter_response = requests.get(f'http://localhost:{default_gateway_port}/api/document/split_trigrams',
                                     params={'content':
                                             Packer.pack({'text': lemmatized_text})}).content.decode('utf-8')
    trigrams = Packer.unpack(splitter_response)['response']['trigrams']

    return unigrams, bigrams, trigrams


unigrams, bigrams, trigrams = prepare_text(input('text: '))
default_port = 5004

unigrams_response = requests.get(f'http://localhost:{default_port}/api/featureExtraction/unigramsWeight',
                                 params={'content': Packer.pack({'unigrams': unigrams})}).content.decode('utf-8')

response = Packer.unpack(unigrams_response)['response']
unigrams_weight = response['unigrams_weight']
print(unigrams_weight)
