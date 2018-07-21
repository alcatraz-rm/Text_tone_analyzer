# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import os
import csv
import math
import sys
sys.path.append(os.path.join('..', '..'))

from Python.Services.DatabaseCursor import DatabaseCursor
from Python.Services.NgramAnalyzer import NgramAnalyzer
from Python.Services.Logger import Logger


class TextWeightCounter:
    def __init__(self):
        self.docs_count = dict()
        self.count_all_docs()

        self.database_cursor = DatabaseCursor()
        self.ngram_analyzer = NgramAnalyzer()
        self.logger = Logger()

        if not self.logger.configured:
            self.logger.configure()

    @staticmethod
    def count_docs_in_dataset(mode):
        with open(os.path.join('..', '..', 'Databases', 'dataset_with_%s.csv' % mode), 'r',
                  encoding='utf-8') as file:
            positive_docs = 0
            negative_docs = 10000
            for row in csv.reader(file):
                if ''.join(row).split(';')[1] == 'positive':
                    positive_docs += 1
                else:
                    negative_docs += 1

        return positive_docs + negative_docs - 10000, positive_docs, negative_docs

    def count_all_docs(self):
        modes = ['unigrams', 'bigrams', 'trigrams']
        for mode in modes:
            self.docs_count[mode] = dict()
            self.docs_count[mode]['all_docs'], self.docs_count[mode]['positive_docs'], \
                self.docs_count[mode]['negative_docs'] = self.count_docs_in_dataset(mode)

    @staticmethod
    def detect_ngram_type(ngram):
        if ngram.count(' ') == 0:
            return 'unigram'
        elif ngram.count(' ') == 1:
            return 'bigram'
        elif ngram.count(' ') == 2:
            return 'trigram'

    def count_ngram_weight(self, ngram):
        ngram_type = self.detect_ngram_type(ngram)

        # if self.database_cursor.entry_exists(ngram):
        pos_docs_word, neg_docs_word = self.database_cursor.get_info(ngram)
        # else:
            # pos_docs_word, neg_docs_word = self.ngram_analyzer.relevant_ngram_find(ngram)

        if (not (pos_docs_word and neg_docs_word)) or (pos_docs_word == 1 and neg_docs_word == 1):
            return 0

        delta_tf_idf = math.log10((self.docs_count[ngram_type + 's']['negative_docs'] * pos_docs_word) /
                                  (self.docs_count[ngram_type + 's']['positive_docs'] * neg_docs_word))

        return delta_tf_idf

    def count_weight_by_unigrams(self, unigrams):
        checked_unigrams = list()
        important_unigrams = list()
        unigrams_weight = 0

        for unigram in unigrams:
            if unigram not in checked_unigrams:
                this_doc_unigram = unigrams.count(unigram)
                unigram_weight = this_doc_unigram * self.count_ngram_weight(unigram)
                unigrams_weight += unigram_weight
                checked_unigrams.append(unigram)

                if unigram_weight:
                    important_unigrams.append(unigram)

        if len(important_unigrams) >= round(len(unigrams) * 0.6) and important_unigrams:
            return unigrams_weight / len(important_unigrams)

        else:
            return None

    def count_weight_by_bigrams(self, bigrams):
        if not bigrams:
            return None

        checked_bigrams = list()
        important_bigrams = list()
        bigrams_weight = 0

        for bigram in bigrams:
            if bigram not in checked_bigrams:
                this_doc_bigram = bigrams.count(bigram)
                bigram_weight = this_doc_bigram * self.count_ngram_weight(bigram)
                bigrams_weight += bigram_weight
                checked_bigrams.append(bigram)

                if bigram_weight:
                    important_bigrams.append(bigram)

        if len(important_bigrams) >= len(bigrams) // 2 and important_bigrams:
            return bigrams_weight / len(important_bigrams)

        else:
            return None

    def count_weight_by_trigrams(self, trigrams):
        if not trigrams:
            return None

        checked_trigrams = list()
        important_trigrams = list()
        trigrams_weight = 0

        for trigram in trigrams:
            if trigram not in checked_trigrams:
                this_doc_trigram = trigrams.count(trigram)
                trigram_weight = this_doc_trigram * self.count_ngram_weight(trigram)
                trigrams_weight += trigram_weight
                checked_trigrams.append(trigram)

                if trigram_weight:
                    important_trigrams.append(trigram)

        if len(important_trigrams) >= round(len(trigrams) * 0.4) and important_trigrams:
            return trigrams_weight / len(important_trigrams)

        else:
            return None
