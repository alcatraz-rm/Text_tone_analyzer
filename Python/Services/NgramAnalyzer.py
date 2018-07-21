# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import os
import sys
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import re
import pymorphy2
sys.path.append(os.path.join('..', '..'))

from Python.Services.DatabaseCursor import DatabaseCursor
from Python.Services.Logger import Logger


class NgramAnalyzer:
    def __init__(self):
        self.vec_model = None
        self.load_vec_model()

        self.database_cursor = DatabaseCursor()
        self.logger = Logger()

        if not self.logger.configured:
            self.logger.configure()

    def load_vec_model(self):
        if os.getcwd().endswith('Master') and os.getcwd().endswith('Tests') and\
                os.path.exists(os.path.join('..', '..', 'Databases', 'ruscorpora_upos_skipgram_300_10_2017.bin.gz')):

            self.vec_model = gensim.models.KeyedVectors.load_word2vec_format(os.path.join('..', '..', 'Databases',
                                                                                     'ruscorpora_upos_skipgram_300_10_2017.bin.gz'),
                                                                        binary=True)

    @staticmethod
    def part_of_speech_detect(word):
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

    def nearest_synonyms_find(self, word, topn):
        nearest_synonyms = list()
        part_of_speech = self.part_of_speech_detect(word)
        if part_of_speech:
            word = word + '_%s' % self.part_of_speech_detect(word)

        for word in self.vec_model.most_similar(positive=[word], topn=topn):
            nearest_synonyms.append({'word': word[0].split('_')[0], 'cosine proximity': word[1]})

            return nearest_synonyms

    def relevant_ngram_find(self, ngram):
        cwd = os.getcwd()

        if ngram.count(' ') == 0:
            nearest_synonyms = self.nearest_synonyms_find(ngram, 10)
            if nearest_synonyms:
                for nearest_synonym in nearest_synonyms:
                    data = self.database_cursor.get_info(nearest_synonym)
                    if data:
                        print(data[0])
                        return data[1], data[2]

        elif ngram.count(' ') == 1:
            words = ngram.split()

            nearest_synonyms_word1 = self.nearest_synonyms_find(words[0], 10)
            nearest_synonyms_word2 = self.nearest_synonyms_find(words[1], 10)

            for nearest_synonym_word1 in nearest_synonyms_word1:
                for nearest_synonym_word2 in nearest_synonyms_word2:
                    data = self.database_cursor.get_info(nearest_synonym_word1 + ' '
                                                         + nearest_synonym_word2)

                    if data:
                        print(data[0])
                        return data[1], data[2]

        elif ngram.count(' ') == 2:
            words = ngram.split()

            nearest_synonyms_word1 = self.nearest_synonyms_find(words[0], 10)
            nearest_synonyms_word2 = self.nearest_synonyms_find(words[1], 10)
            nearest_synonyms_word3 = self.nearest_synonyms_find(words[2], 10)

            for nearest_synonym_word1 in nearest_synonyms_word1:
                for nearest_synonym_word2 in nearest_synonyms_word2:
                    for nearest_synonym_word3 in nearest_synonyms_word3:
                        data = self.database_cursor.get_info(nearest_synonym_word1 + ' '
                                                             + nearest_synonym_word2 + ' ' + nearest_synonym_word3)

                        if data:
                            print(data[0])
                            return data[1], data[2]

        return None, None
