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
from Python.Services.DatabaseCursor import DatabaseCursor
from Python.Services.NgramAnalyzer import NgramAnalyzer
from Python.Services.Logger import Logger
from Python.Services.PathService import PathService


class TextWeightCounter:
    def __init__(self):
        self._docs_count = dict()

        self._database_cursor = DatabaseCursor()
        self._ngram_analyzer = NgramAnalyzer()
        self.__logger = Logger()
        self._path_service = PathService()

        if not self.__logger.configured:
            self.__logger.configure()

        self._count_all_docs()

        self.__logger.info('TextWeightCounter was successfully initialized.', 'TextWeightCounter.__init__()')

    def _count_docs_in_dataset(self, mode):
        path_to_dataset = self._path_service.get_path_to_dataset('dataset_with_%s.csv' % mode)

        with open(path_to_dataset, 'r', encoding='utf-8') as file:
            positive_docs = 0
            negative_docs = 10000

            for row in csv.reader(file):
                if ''.join(row).split(';')[1] == 'positive':
                    positive_docs += 1
                else:
                    negative_docs += 1

        return positive_docs + negative_docs - 10000, positive_docs, negative_docs

    def _count_all_docs(self):
        modes = ['unigrams', 'bigrams', 'trigrams']

        for mode in modes:
            self._docs_count[mode] = dict()
            self._docs_count[mode]['all_docs'], self._docs_count[mode]['positive_docs'], \
                self._docs_count[mode]['negative_docs'] = self._count_docs_in_dataset(mode)

    @staticmethod
    def _detect_ngram_type(ngram):
        if ngram.count(' ') == 0:
            return 'unigram'

        elif ngram.count(' ') == 1:
            return 'bigram'

        elif ngram.count(' ') == 2:
            return 'trigram'

    def _count_ngram_weight(self, ngram):
        self.__logger.info('Ngram: %s' % ngram, 'TextWeightCounter._count_ngram_weight()')

        ngram_type = self._detect_ngram_type(ngram)
        delta_tf_idf = 0

        self.__logger.info('Ngram_type: %s' % ngram_type, 'TextWeightCounter._count_ngram_weight()')

        if self._database_cursor.entry_exists(ngram):
            pos_docs_word, neg_docs_word = self._database_cursor.get_info(ngram)

            delta_tf_idf = math.log10((self._docs_count[ngram_type + 's']['negative_docs'] * pos_docs_word) /
                                      (self._docs_count[ngram_type + 's']['positive_docs'] * neg_docs_word))

        else:
            response = self._ngram_analyzer.relevant_ngram_find(ngram)

            if response['synonym_found']:

                if ngram_type == 'unigram':
                    pos_docs_word, neg_docs_word = response['content']['pos_docs'], response['content']['neg_docs']

                    if (not (pos_docs_word and neg_docs_word)) or (pos_docs_word == 1 and neg_docs_word == 1):
                        return 0

                    delta_tf_idf = math.log10((self._docs_count[ngram_type + 's']['negative_docs'] * pos_docs_word) /
                                              (self._docs_count[ngram_type + 's']['positive_docs'] * neg_docs_word))

        return delta_tf_idf

    def count_weight_by_unigrams(self, unigrams):
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

            self.__logger.info('Unigrams weight: %f' % unigrams_weight,
                               'TextWeightCounter.count_weight_by_unigrams()')

            return unigrams_weight

    def count_weight_by_bigrams(self, bigrams):
        if not bigrams:
            return None

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

            self.__logger.info('Bigrams weight: %f' % bigrams_weight,
                               'TextWeightCounter.count_weight_by_bigrams()')

            return bigrams_weight

    def count_weight_by_trigrams(self, trigrams):
        if not trigrams:
            return None

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
            
            self.__logger.info('Trigrams weight: %f' % trigrams_weight,
                               'TextWeightCounter.count_weight_by_trigrams()')

            return trigrams_weight
