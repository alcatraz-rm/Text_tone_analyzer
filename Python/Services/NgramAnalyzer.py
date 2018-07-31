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
import requests
from Python.Services.DatabaseCursor import DatabaseCursor
from Python.Services.Logger import Logger
from Python.Services.Lemmatizer.Lemmatizer import Lemmatizer


class NgramAnalyzer:
    def __init__(self):
        self._vec_model = None

        self._database_cursor = DatabaseCursor()
        self.__logger = Logger()
        self._lemmatizer = Lemmatizer()

        if not self.__logger.configured:
            self.__logger.configure()

        self._load_vec_model()

        self.__logger.info('NgramAnalyzer was successfully initialized.', 'NgramAnalyzer.__init__()')

    def _load_vec_model(self):
        if not os.path.exists(os.path.join('..', 'Databases', 'ruscorpora_upos_skipgram_300_10_2017.bin.gz')) and not \
           os.path.exists(os.path.join('..', '..', '..', 'Databases', 'ruscorpora_upos_skipgram_300_10_2017.bin.gz')):

            self.__logger.warning("Vector model doesn't exist.", "NgramAnalyzer._load_vec_model()")

            try:
                self._download_vector_model()
            except SystemError:
                self.__logger.fatal('Problems with connection.', 'NgramAnalyzer._load_vec_model()')

            self.__logger.info('Vector model was successfully downloaded.', 'NgramAnalyzer._load_vec_model()')

        if os.getcwd().endswith('Python'):
            self._vec_model = gensim.models.KeyedVectors.load_word2vec_format(
                                                            os.path.join('..', 'Databases',
                                                                         'ruscorpora_upos_skipgram_300_10_2017.bin.gz'),
                                                            binary=True)

        elif os.getcwd().endswith(os.path.join('Tests', 'System')):

            self._vec_model = gensim.models.KeyedVectors.load_word2vec_format(
                                                            os.path.join('..', '..', '..', 'Databases',
                                                                         'ruscorpora_upos_skipgram_300_10_2017.bin.gz'),
                                                            binary=True)

    @staticmethod
    def _download_vector_model():
        request_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download'
        vector_model_url = 'https://yadi.sk/d/qoxAdYUC3ZcyrN'

        download_url = requests.get(request_url, params={
            'public_key': vector_model_url
        }).json()["href"]

        response = requests.get(download_url)

        vector_model_path = 'ruscorpora_upos_skipgram_300_10_2017.bin.gz'

        if os.getcwd().endswith('Python'):
            vector_model_path = os.path.join('..', 'Databases', 'ruscorpora_upos_skipgram_300_10_2017.bin.gz')
        elif os.getcwd().endswith(os.path.join('Tests', 'System')):
            vector_model_path = os.path.join('..', '..', '..', 'Databases', 'ruscorpora_upos_skipgram_300_10_2017.bin.gz')

        with open(vector_model_path, 'wb') as vec_model:
            vec_model.write(response.content)

    @staticmethod
    def _part_of_speech_detect(word):
        part_of_speech = pymorphy2.MorphAnalyzer().parse(word)[0].tag.POS

        if part_of_speech:
            if re.match(r'ADJ', part_of_speech):
                return 'ADJ'

            elif re.match(r'PRT', part_of_speech):
                return 'PRT'

            if part_of_speech == 'NOUN':
                return 'NOUN'

            elif part_of_speech == 'INFN':
                return 'VERB'

            elif part_of_speech == 'ADVB' or part_of_speech == 'PRED':
                return 'ADV'

            elif part_of_speech == 'PRCL':
                return 'PART'

    @staticmethod
    def _detect_ngram_type(ngram):
        if ngram.count(' ') == 0:
            return 'unigram'
        elif ngram.count(' ') == 1:
            return 'bigram'
        elif ngram.count(' ') == 2:
            return 'trigram'

    def _nearest_synonyms_find(self, word, topn):
        if not self._vec_model:
            return None

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

        except KeyError:
            return None

        return nearest_synonyms

    def relevant_ngram_find(self, ngram):
        self.__logger.info('Start ngram: %s' % ngram, 'NgramAnalyzer.relevant_ngram_find()')

        response = {'synonym_found': False, 'content': dict()}

        if ngram.count(' ') == 0:
            nearest_synonyms = self._nearest_synonyms_find(ngram, 10)

            if not nearest_synonyms:
                return response

            for nearest_synonym in nearest_synonyms:
                data = self._database_cursor.get_info(nearest_synonym['word'])

                if data[0]:
                    self.__logger.info('Relevant ngram: %s' % nearest_synonym['word'],
                                       'NgramAnalyzer.relevant_ngram_find()')

                    response['synonym_found'] = True

                    response['content']['synonym'] = nearest_synonym['word']
                    response['content']['pos_docs'] = data[0]
                    response['content']['neg_docs'] = data[1]

                    return response

        # elif ngram.count(' ') == 1:
        #     synonym_word1 = None
        #     synonym_word2 = None
        #
        #     words = ngram.split()
        #
        #     nearest_synonyms_word1 = self._nearest_synonyms_find(words[0], 10)
        #     nearest_synonyms_word2 = self._nearest_synonyms_find(words[1], 10)
        #
        #     if not nearest_synonyms_word1 or not nearest_synonyms_word2:
        #         return None, None, None
        #
        #     for nearest_synonym in nearest_synonyms_word1:
        #         data = self._database_cursor.get_info(nearest_synonym['word'])
        #
        #         if data[0]:
        #             synonym_word2 = [nearest_synonym['word']]
        #             synonym_word2.extend(list(data))
        #
        #     for nearest_synonym in nearest_synonyms_word2:
        #         data = self._database_cursor.get_info(nearest_synonym['word'])
        #
        #         if data[0]:
        #             synonym_word2 = [nearest_synonym['word']]
        #             synonym_word2.extend(list(data))
        #
        #     if synonym_word1 and synonym_word2:
        #         response['synonym_found'] = True
        #
        #         response['content']['word_1'] = {'word': synonym_word1[0], 'pos_count': synonym_word1[1],
        #                                          'neg_count': synonym_word1[2]}
        #
        #         response['content']['word_2'] = {'word': synonym_word2[0], 'pos_count': synonym_word2[1],
        #                                          'neg_count': synonym_word2[2]}

        return response
