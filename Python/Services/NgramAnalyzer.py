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
import re

import gensim
import pymorphy2

from Python.Services.Configurator import Configurator
from Python.Services.DatabaseCursor import DatabaseCursor
from Python.Services.Lemmatizer.Lemmatizer import Lemmatizer
from Python.Services.Logger import Logger
from Python.Services.PathService import PathService
from Python.Services.ExceptionsHandler import ExceptionsHandler


class NgramAnalyzer:
    def __init__(self):
        # Services
        self._database_cursor = DatabaseCursor()
        self.__logger = Logger()
        self._exceptions_hanlder = ExceptionsHandler()
        self._lemmatizer = Lemmatizer()
        self._path_service = PathService()
        self._configurator = Configurator()

        # Data
        self._vec_model = None

        self._load_vec_model()

        self.__logger.info('NgramAnalyzer was successfully initialized.', 'NgramAnalyzer.__init__()')

    def _load_vec_model(self):
        if not self._path_service.path_to_vector_model:
            self.__logger.warning("Vector model doesn't exist.", "NgramAnalyzer._load_vec_model()")

            self._configurator.download_vector_model()
            self._path_service.set_path_to_vector_model(os.path.join(self._path_service.path_to_databases,
                                                                     'ruscorpora_upos_skipgram_300_10_2017.bin.gz'))
            self.__logger.info('Vector model was successfully downloaded.', 'NgramAnalyzer._load_vec_model()')

        if self._path_service.path_to_vector_model:
            self._vec_model = gensim.models.KeyedVectors.load_word2vec_format(self._path_service.path_to_vector_model,
                                                                              binary=True)

    @staticmethod
    def _part_of_speech_detect(word):
        if not word:
            return

        part_of_speech = pymorphy2.MorphAnalyzer().parse(word)[0].tag.POS

        if part_of_speech:
            if re.match(r'ADJ', part_of_speech):
                return 'ADJ'

            elif re.match(r'PRT', part_of_speech):
                return 'PRT'

            elif part_of_speech == 'INFN':
                return 'VERB'

            elif part_of_speech == 'ADVB' or part_of_speech == 'PRED':
                return 'ADV'

            elif part_of_speech == 'PRCL':
                return 'PART'

        return part_of_speech

    @staticmethod
    def _detect_ngram_type(ngram):
        if not ngram:
            return

        if ngram.count(' ') == 0:
            return 'unigram'

        elif ngram.count(' ') == 1:
            return 'bigram'

        elif ngram.count(' ') == 2:
            return 'trigram'

    def _nearest_synonyms_find(self, word, topn):
        if not self._vec_model or not word or topn <= 0:
            return

        nearest_synonyms = list()
        part_of_speech = self._part_of_speech_detect(word)
        ngram_type = self._detect_ngram_type(word)

        if part_of_speech:
            word = word + '_%s' % self._part_of_speech_detect(word)

        try:
            for synonym in self._vec_model.most_similar(positive=[word], topn=topn * 10):
                found_synonym = self._lemmatizer.lead_to_initial_form(synonym[0].split('_')[0])

                if found_synonym and self._detect_ngram_type(found_synonym) == ngram_type:
                    nearest_synonyms.append({'word': found_synonym,
                                             'cosine proximity': synonym[1]})

                if len(nearest_synonyms) == topn:
                    break

        except BaseException as exception:
            self.__logger.error(self._exceptions_hanlder.get_error_message(exception),
                                'NgramAnalyzer._nearest_synonyms_find()')
            return

        return nearest_synonyms

    def relevant_ngram_find(self, ngram):
        if not ngram:
            return

        self.__logger.info(f'Start ngram: {ngram}', 'NgramAnalyzer.relevant_ngram_find()')

        response = {'synonym_found': False, 'content': dict()}

        if self._detect_ngram_type(ngram) == 'unigram':
            synonyms_count = 10
            nearest_synonyms = self._nearest_synonyms_find(ngram, synonyms_count)

            if not nearest_synonyms:
                return response

            for nearest_synonym in nearest_synonyms:
                data = self._database_cursor.get_info(nearest_synonym['word'])

                if data and data[0]:
                    self.__logger.info(f'Relevant ngram: {nearest_synonym["word"]}',
                                       'NgramAnalyzer.relevant_ngram_find()')

                    response['synonym_found'] = True

                    response['content']['synonym'] = nearest_synonym['word']
                    response['content']['pos_docs'] = data[0]
                    response['content']['neg_docs'] = data[1]

                    return response

        return response
