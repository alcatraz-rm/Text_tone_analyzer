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
default_port = 5004


def prepare_text(text):
    lemmatizer_response = requests.get(f'http://localhost:{default_port}/api/lemmatizer/getTextInitialForm',
                                       params={'content':
                                               Packer.pack({'text': text})}).content.decode('utf-8')
    lemmatized_text = Packer.unpack(lemmatizer_response)['response']['lemmatized_text']

    splitter_response = requests.get(f'http://localhost:{default_port}/api/document/split_unigrams',
                                     params={'content':
                                             Packer.pack({'text': lemmatized_text})}).content.decode('utf-8')
    unigrams = Packer.unpack(splitter_response)['response']['unigrams']

    splitter_response = requests.get(f'http://localhost:{default_port}/api/document/split_bigrams',
                                     params={'content':
                                             Packer.pack({'text': lemmatized_text})}).content.decode('utf-8')
    bigrams = Packer.unpack(splitter_response)['response']['bigrams']

    splitter_response = requests.get(f'http://localhost:{default_port}/api/document/split_trigrams',
                                     params={'content':
                                             Packer.pack({'text': lemmatized_text})}).content.decode('utf-8')
    trigrams = Packer.unpack(splitter_response)['response']['trigrams']

    return unigrams, bigrams, trigrams


def count_weights(text):
    unigrams, bigrams, trigrams = prepare_text(text)

    unigrams_response = requests.get(f'http://localhost:{default_port}/api/featureExtraction/unigramsWeight',
                                     params={'content': Packer.pack({'unigrams': unigrams})}).content.decode('utf-8')

    response = Packer.unpack(unigrams_response)['response']
    unigrams_weight = response['unigrams_weight']

    bigrams_response = requests.get(f'http://localhost:{default_port}/api/featureExtraction/bigramsWeight',
                                    params={'content': Packer.pack({'bigrams': bigrams})}).content.decode('utf-8')

    response = Packer.unpack(bigrams_response)['response']
    bigrams_weight = response['bigrams_weight']

    trigrams_response = requests.get(f'http://localhost:{default_port}/api/featureExtraction/trigramsWeight',
                                     params={'content': Packer.pack({'trigrams': trigrams})}).content.decode('utf-8')

    response = Packer.unpack(trigrams_response)['response']
    trigrams_weight = response['trigrams_weight']

    return unigrams_weight, bigrams_weight, trigrams_weight


def predict_tonal(unigrams_weight, bigrams_weight, trigrams_weight):
    unigrams_weight = unigrams_weight or 0
    bigrams_weight = bigrams_weight or 0
    trigrams_weight = trigrams_weight or 0

    print(unigrams_weight, bigrams_weight, trigrams_weight)

    response = requests.get(f'http://localhost:{default_port}/api/classifier/predict',
                            params={'content':
                                    Packer.pack({'unigrams_weight': str(unigrams_weight),
                                                 'bigrams_weight': str(bigrams_weight),
                                                 'trigrams_weight': str(trigrams_weight)})}).content.decode('utf-8')
    response = Packer.unpack(response)

    print(response)
    return response['response']['tonal'], response['response']['probability']


text = input('text: ')
unigrams_weight, bigrams_weight, trigrams_weight = count_weights(text)
print(unigrams_weight, bigrams_weight, trigrams_weight)
tonal, probability = predict_tonal(unigrams_weight, bigrams_weight, trigrams_weight)

print(tonal, probability)
