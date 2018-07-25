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
import warnings
import re
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import pymorphy2
from Python.Services.DatabaseCursor import DatabaseCursor
from Python.Services.Logger import Logger


class NgramAnalyzer:
    def __init__(self):
        self._vec_model = None
        self._load_vec_model()

        self._database_cursor = DatabaseCursor()
        self.__logger = Logger()

        if not self.__logger.configured:
            self.__logger.configure()

        self.__logger.info('NgramAnalyzer was successfully initialized.', 'NgramAnalyzer.__init__()')

    def _load_vec_model(self):
        if os.getcwd().endswith('Python') and os.path.exists(
                os.path.join('..', 'Databases', 'ruscorpora_upos_skipgram_300_10_2017.bin.gz')):

            self._vec_model = gensim.models.KeyedVectors.load_word2vec_format(
                                                            os.path.join('..', 'Databases',
                                                                         'ruscorpora_upos_skipgram_300_10_2017.bin.gz'),
                                                            binary=True)

        if os.getcwd().endswith('Tests') and os.path.exists(
                os.path.join('..', '..', 'Databases', 'ruscorpora_upos_skipgram_300_10_2017.bin.gz')):

            self._vec_model = gensim.models.KeyedVectors.load_word2vec_format(
                                                            os.path.join('..', '..', 'Databases',
                                                                         'ruscorpora_upos_skipgram_300_10_2017.bin.gz'),
                                                            binary=True)

    @staticmethod
    def _part_of_speech_detect(word):
        part_of_speech = pymorphy2.MorphAnalyzer().parse(word)[0].tag.POS

        if part_of_speech:
            if re.match(r'ADJ', part_of_speech):
                return 'ADJ'

            elif re.match(r'PRT', part_of_speech):
                return 'PRT'

            elif part_of_speech == 'INFN':
                return 'VERB'

            elif part_of_speech == 'ADVB':
                return 'ADV'

    def _nearest_synonyms_find(self, word, topn):
        nearest_synonyms = list()
        part_of_speech = self._part_of_speech_detect(word)
        if part_of_speech:
            word = word + '_%s' % self._part_of_speech_detect(word)

        try:
            for synonym in self._vec_model.most_similar(positive=[word], topn=topn):
                nearest_synonyms.append({'word': synonym[0].split('_')[0], 'cosine proximity': synonym[1]})

        except KeyError:
            return None

        return nearest_synonyms

    def relevant_ngram_find(self, ngram):
        self.__logger.info('Start ngram: %s' % ngram, 'NgramAnalyzer.relevant_ngram_find()')

        if ngram.count(' ') == 0:
            nearest_synonyms = self._nearest_synonyms_find(ngram, 10)

            if not nearest_synonyms:
                return None, None

            for nearest_synonym in nearest_synonyms:
                data = self._database_cursor.get_info(nearest_synonym['word'])
                if data[0]:
                    self.__logger.info('Relevant ngram: %s' % data[0], 'NgramAnalyzer.relevant_ngram_find()')
                    return data[0], data[1]

        elif ngram.count(' ') == 1:
            words = ngram.split()

            nearest_synonyms_word1 = self._nearest_synonyms_find(words[0], 5)
            nearest_synonyms_word2 = self._nearest_synonyms_find(words[1], 5)

            if not nearest_synonyms_word1 or not nearest_synonyms_word2:
                return None, None

            for nearest_synonym_word1 in nearest_synonyms_word1:
                for nearest_synonym_word2 in nearest_synonyms_word2:
                    data = self._database_cursor.get_info(nearest_synonym_word1['word'] + ' '
                                                          + nearest_synonym_word2['word'])

                    if data[0]:
                        self.__logger.info('Relevant ngram: %s' % data[0], 'NgramAnalyzer.relevant_ngram_find()')
                        return data[0], data[1]

        elif ngram.count(' ') == 2:
            words = ngram.split()

            nearest_synonyms_word1 = self._nearest_synonyms_find(words[0], 3)
            nearest_synonyms_word2 = self._nearest_synonyms_find(words[1], 3)
            nearest_synonyms_word3 = self._nearest_synonyms_find(words[2], 3)

            if not nearest_synonyms_word1 or not nearest_synonyms_word2 or not nearest_synonyms_word3:
                return None, None

            for nearest_synonym_word1 in nearest_synonyms_word1:
                for nearest_synonym_word2 in nearest_synonyms_word2:
                    for nearest_synonym_word3 in nearest_synonyms_word3:
                        data = self._database_cursor.get_info(nearest_synonym_word1['word'] + ' '
                                                              + nearest_synonym_word2['word'] + ' '
                                                              + nearest_synonym_word3['word'])

                        if data[0]:
                            self.__logger.info('Relevant ngram: %s' % data[0], 'NgramAnalyzer.relevant_ngram_find()')
                            return data[0], data[1]

        self.__logger.info('Cannot find relevant ngram', 'NgramAnalyzer.relevant_ngram_find()')
        return None, None
