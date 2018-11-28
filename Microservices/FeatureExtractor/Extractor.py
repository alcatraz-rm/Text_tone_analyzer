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

import csv
import math
import os

import requests
from flask import Flask, request
import logging

from Microservices import Logger, Packer

logger = Logger.Logger()
server = Flask(__name__)
default_port = 5005


class TextWeightCounter:
    def __init__(self):
        # Services

        # Data
        self._docs_count = dict()
        self._path_to_datasets = TextWeightCounter._find_datasets()

        self._count_all_docs()

        logger.info('TextWeightCounter was successfully initialized.', __name__)

    @staticmethod
    def _find_datasets():
        wd = os.getcwd()

        while 'Data' not in os.listdir(os.getcwd()):
            os.chdir('..')

        path_to_datasets = os.path.join(os.getcwd(), 'Data', 'Datasets')

        os.chdir(wd)
        return path_to_datasets

    def _count_docs_in_dataset(self, mode: str):
        path_to_dataset = os.path.join(self._path_to_datasets, f'dataset_with_{mode}.csv')

        with open(path_to_dataset, 'r', encoding='utf-8') as file:
            negative_docs_shift = 10000

            positive_docs = 0
            negative_docs = negative_docs_shift

            for row in csv.reader(file):
                if ''.join(row).split(';')[1] == 'positive':
                    positive_docs += 1
                else:
                    negative_docs += 1

        return positive_docs + negative_docs - negative_docs_shift, positive_docs, negative_docs

    def _count_all_docs(self):
        modes = ['unigrams', 'bigrams', 'trigrams']

        for mode in modes:
            self._docs_count[mode] = dict()
            self._docs_count[mode]['all_docs'], self._docs_count[mode]['positive_docs'], \
            self._docs_count[mode]['negative_docs'] = self._count_docs_in_dataset(mode)

    @staticmethod
    def _detect_ngram_type(ngram: str):
        if ngram.count(' ') == 0:
            return 'unigram'

        elif ngram.count(' ') == 1:
            return 'bigram'

        elif ngram.count(' ') == 2:
            return 'trigram'

    @staticmethod
    def get_entry_from_db(ngram):
        default_port = 5004
        data = Packer.pack({'ngram': ngram})

        response = requests.get(f'http://localhost:{default_port}/api/database/getData', params=
        {'content': data}).content.decode('utf-8')

        return Packer.unpack(response)['response']['pos_count'], \
               Packer.unpack(response)['response']['neg_count']

    @staticmethod
    def entry_exists_in_db(ngram):
        default_port = 5004
        data = Packer.pack({'ngram': ngram})

        response = requests.get(f'http://localhost:{default_port}/api/database/entryExists', params=
        {'content': data}).content.decode('utf-8')

        return Packer.unpack(response)['response']['entry_exist']

    def _count_ngram_weight(self, ngram: str):
        logger.info(f'Ngram: {ngram}', __name__)

        ngram_type = self._detect_ngram_type(ngram)
        delta_tf_idf = 0

        logger.info(f'Ngram_type: {ngram_type}', __name__)

        if TextWeightCounter.entry_exists_in_db(ngram):
            pos_docs_word, neg_docs_word = TextWeightCounter.get_entry_from_db(ngram)

            delta_tf_idf = math.log10((self._docs_count[ngram_type + 's']['negative_docs'] * pos_docs_word) /
                                      (self._docs_count[ngram_type + 's']['positive_docs'] * neg_docs_word))

        # else:
        #     response = self._ngram_analyzer.relevant_ngram_find(ngram)
        #
        #     if response['synonym_found']:
        #
        #         if ngram_type == 'unigram':
        #             pos_docs_word, neg_docs_word = response['content']['pos_docs'], response['content']['neg_docs']
        #
        #             if (not (pos_docs_word and neg_docs_word)) or (pos_docs_word == 1 and neg_docs_word == 1):
        #                 return 0
        #
        #             delta_tf_idf = math.log10((self._docs_count[ngram_type + 's']['negative_docs'] * pos_docs_word) /
        #                                       (self._docs_count[ngram_type + 's']['positive_docs'] * neg_docs_word))

        return delta_tf_idf

    def count_weight_by_unigrams(self, unigrams: list):
        checked_unigrams = list()
        important_unigrams = list()
        unigrams_weight = 0

        for unigram in unigrams:
            if unigram not in checked_unigrams:
                this_doc_unigram = unigrams.count(unigram)
                unigram_weight = this_doc_unigram * self._count_ngram_weight(unigram)
                unigrams_weight += unigram_weight

                checked_unigrams.append(unigram)

                if unigram_weight:
                    important_unigrams.append(unigram)

        if len(important_unigrams) >= round(len(unigrams) * 0.6) and important_unigrams:
            unigrams_weight = unigrams_weight / len(important_unigrams)

            logger.info(f'Unigrams weight: {unigrams_weight}', __name__)

            return unigrams_weight

    def count_weight_by_bigrams(self, bigrams: list):
        if not bigrams:
            return

        checked_bigrams = list()
        important_bigrams = list()
        bigrams_weight = 0

        for bigram in bigrams:
            if bigram not in checked_bigrams:
                this_doc_bigram = bigrams.count(bigram)
                bigram_weight = this_doc_bigram * self._count_ngram_weight(bigram)
                bigrams_weight += bigram_weight

                checked_bigrams.append(bigram)

                if bigram_weight:
                    important_bigrams.append(bigram)

        if len(important_bigrams) >= len(bigrams) // 2 and important_bigrams:
            bigrams_weight = bigrams_weight / len(important_bigrams)

            logger.info(f'Bigrams weight: {bigrams_weight}', __name__)

            return bigrams_weight

    def count_weight_by_trigrams(self, trigrams: list):
        if not trigrams:
            return

        checked_trigrams = list()
        important_trigrams = list()
        trigrams_weight = 0

        for trigram in trigrams:
            if trigram not in checked_trigrams:
                this_doc_trigram = trigrams.count(trigram)
                trigram_weight = this_doc_trigram * self._count_ngram_weight(trigram)
                trigrams_weight += trigram_weight

                checked_trigrams.append(trigram)

                if trigram_weight:
                    important_trigrams.append(trigram)

        if len(important_trigrams) >= round(len(trigrams) * 0.4) and important_trigrams:
            trigrams_weight = trigrams_weight / len(important_trigrams)

            logger.info(f'Trigrams weight: {trigrams_weight}', __name__)

            return trigrams_weight

    def __del__(self):
        del self._docs_count


text_weight_counter = TextWeightCounter()


@server.route('/api/featureExtraction/unigramsWeight', methods=['GET'])
def count_unigrams_weight():
    logger.info(f'{request.method} request.', __name__)
    response = dict(response=dict(code=400))

    if 'content' in request.args:
        content = Packer.unpack(request.args['content'])
        logger.info(f'Params: {str(content)}', __name__)
    else:
        logger.error('Bad request.', __name__)
        return Packer.pack(response)

    if 'unigrams' in content and content['unigrams']:
        unigrams = content['unigrams']
        response['response']['code'] = 200
        response['response']['unigrams_weight'] = text_weight_counter.count_weight_by_unigrams(unigrams)

    return Packer.pack(response)


@server.route('/api/featureExtraction/bigramsWeight', methods=['GET'])
def count_bigrams_weight():
    logger.info(f'{request.method} request.', __name__)
    response = dict(response=dict(code=400))

    if 'content' in request.args:
        content = Packer.unpack(request.args['content'])
        logger.info(f'Params: {str(content)}', __name__)
    else:
        logger.error('Bad request.', __name__)
        return Packer.pack(response)

    if 'bigrams' in content and content['bigrams']:
        bigrams = content['bigrams']
        response['response']['code'] = 200
        response['response']['bigrams_weight'] = text_weight_counter.count_weight_by_bigrams(bigrams)

    return Packer.pack(response)


@server.route('/api/featureExtraction/trigramsWeight', methods=['GET'])
def count_trigrams_weight():
    logger.info(f'{request.method} request.', __name__)
    response = dict(response=dict(code=400))

    if 'content' in request.args:
        content = Packer.unpack(request.args['content'])
        logger.info(f'Params: {str(content)}', __name__)
    else:
        logger.error('Bad request.', __name__)
        return Packer.pack(response)

    if 'trigrams' in content and content['trigrams']:
        trigrams = content['trigrams']
        response['response']['code'] = 200
        response['response']['trigrams_weight'] = text_weight_counter.count_weight_by_trigrams(trigrams)

    return Packer.pack(response)


try:
    server.run(port=default_port)
    server.logger.setLevel(logging.CRITICAL)

except BaseException as exception:
    logger.fatal(f'Error while trying to start server: {str(exception)}', __name__)
