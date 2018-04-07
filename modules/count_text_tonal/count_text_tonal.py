# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

from modules.lemmatization.lemmatization import lemmatization
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
from modules.get_ngram_info.get_ngram_info import get_ngram_info
import math
import logging
import pandas
import os
from os import path

docs_count = 103582  # hardcode
cwd = os.getcwd()


class Document:
    def __init__(self, text, vec_model):
        logging.info('\nDocument was successfully initialized\n')
        self.text = lemmatization(text)
        self.unigrams = self.text.split()
        self.bigrams = list()
        self.trigrams = list()
        self.unigrams_weight = 0
        self.unigrams_weight_tf_idf = 0
        self.bigrams_weight = 0
        self.bigrams_weight_tf_idf = 0
        self.trigrams_weight = 0
        self.trigrams_weight_tf_idf = 0
        self.tonal = None
        self.vec_model = vec_model
        self.probability = None
        self.classifier = LogisticRegression()
        self.unigrams_tf_idf = dict()
        self.bigrams_tf_idf = dict()
        self.trigrams_tf_idf = dict()
        self.training_data = dict()

        # self.read_training_data()

    def unigrams_tf_idf_count(self):
        tf_text = dict()
        idf_text = dict()
        checked_unigrams = list()

        # TF count
        for word in self.unigrams:
            tf_text[word] = self.unigrams.count(word) / len(self.unigrams)
            checked_unigrams.append(word)

        # IDF count
        for word in self.unigrams:
            data = get_ngram_info(word, self.vec_model)

            try:
                idf_text[word] = math.log10(docs_count / (data[0] + data[1]))
            except ZeroDivisionError:
                idf_text[word] = 0

        # TF-IDF count
        for word in self.unigrams:
            self.unigrams_tf_idf[word] = tf_text[word] * idf_text[word]

        logging.info('\nunigrams TF IDF was successfully counted\n')

    def bigrams_tf_idf_count(self):
        tf_text = dict()
        idf_text = dict()
        checked_bigrams = list()

        # TF count
        for bigram in self.bigrams:
            tf_text[bigram] = self.bigrams.count(bigram) / len(self.bigrams)
            checked_bigrams.append(bigram)

        # IDF count
        for bigram in self.bigrams:
            data = get_ngram_info(bigram, self.vec_model)

            try:
                idf_text[bigram] = math.log10(docs_count / (data[0] + data[1]))
            except ZeroDivisionError:
                idf_text[bigram] = 0

        # TF-IDF count
        for bigram in self.bigrams:
            self.bigrams_tf_idf[bigram] = tf_text[bigram] * idf_text[bigram]

        logging.info('\nbigrams TF IDF was successfully counted\n')

    def trigrams_tf_idf_count(self):
        tf_text = dict()
        idf_text = dict()
        checked_trigrams = list()

        # TF count
        for trigram in self.trigrams:
            tf_text[trigram] = self.trigrams.count(trigram) / len(self.trigrams)
            checked_trigrams.append(trigram)

        # IDF count
        for trigram in self.trigrams:
            data = get_ngram_info(trigram, self.vec_model)

            try:
                idf_text[trigram] = math.log10(docs_count / (data[0] + data[1]))
            except ZeroDivisionError:
                idf_text[trigram] = 0

        # TF-IDF count
        for trigram in self.trigrams:
            self.trigrams_tf_idf[trigram] = tf_text[trigram] * idf_text[trigram]

        logging.info('\ntrigrams TF IDF was successfully counted\n')

    def split_into_bigrams(self):
        for unigram_index in range(len(self.unigrams) - 1):
            self.bigrams.append(self.unigrams[unigram_index] + ' ' + self.unigrams[unigram_index + 1])

    def split_into_trigrams(self):
        for unigram_index in range(len(self.unigrams) - 2):
            self.trigrams.append(self.unigrams[unigram_index] + ' ' + self.unigrams[unigram_index + 1] + ' ' + \
                    self.unigrams[unigram_index + 2])

    def count_ngram_weight(self, ngram):
        pos_docs = 48179  # hardcode
        neg_docs = 65403  # hardcode
        pos_docs_word, neg_docs_word = get_ngram_info(ngram, self.vec_model)

        if (not (pos_docs_word and neg_docs_word)) or (pos_docs_word == 1 and neg_docs_word == 1):
            return 0

        delta_tf_idf = math.log10((neg_docs * pos_docs_word) / (pos_docs * neg_docs_word))
        logging.info('\nN-gram, delta TF-IDF: %s, %f\n' % (ngram, delta_tf_idf))

        return delta_tf_idf

    def count_weight_by_unigrams_tf_idf(self):
        checked_unigrams = list()
        important_unigrams = list()

        for unigram in self.unigrams:
            if unigram not in checked_unigrams:
                unigram_weight = self.unigrams_tf_idf[unigram] * self.count_ngram_weight(unigram)
                self.unigrams_weight_tf_idf += unigram_weight
                checked_unigrams.append(unigram)

                if unigram_weight:
                    important_unigrams.append(unigram)

        if important_unigrams:
            self.unigrams_weight_tf_idf = self.unigrams_weight_tf_idf / len(important_unigrams)
            logging.info('\nweight by unigrams with TF-IDF: %f\n' % self.unigrams_weight_tf_idf)

        else:
            self.unigrams_weight_tf_idf = None
            logging.error('\nimpossible to count weight by unigrams with TF-IDF\n')

    def count_weight_by_unigrams(self):
        checked_unigrams = list()
        important_unigrams = list()

        for unigram in self.unigrams:
            if unigram not in checked_unigrams:
                this_doc_unigram = self.unigrams.count(unigram)
                unigram_weight = this_doc_unigram * self.count_ngram_weight(unigram)
                self.unigrams_weight += unigram_weight
                checked_unigrams.append(unigram)

                if unigram_weight:
                    important_unigrams.append(unigram)

        if important_unigrams:
            self.unigrams_weight = self.unigrams_weight / len(important_unigrams)
            logging.info('\nweight by unigrams: %f\n' % self.unigrams_weight)

        else:
            self.unigrams_weight = None
            logging.error('\nimpossible to count weight by unigrams\n')

    def count_weight_by_bigrams_tf_idf(self):
        pass

    def count_weight_by_bigrams(self):
        if len(self.unigrams) >= 2:
            self.split_into_bigrams()
            checked_bigrams = list()
            important_bigrams = list()

            for bigram in self.bigrams:
                if bigram not in checked_bigrams:
                    this_doc_bigram = self.bigrams.count(bigram)
                    bigram_weight = this_doc_bigram * self.count_ngram_weight(bigram)
                    self.bigrams_weight += bigram_weight
                    checked_bigrams.append(bigram)

                    if bigram_weight:
                        important_bigrams.append(bigram)

            if important_bigrams:
                self.bigrams_weight = self.bigrams_weight / len(important_bigrams)
                logging.info('\nweight by bigrams: %f\n' % self.bigrams_weight)

            else:
                self.bigrams_weight = None
                logging.error('\nimpossible to count weight by bigrams\n')

    def count_weight_by_trigrams_tf_idf(self):
        pass

    def count_weight_by_trigrams(self):
        if len(self.unigrams) >= 3:
            self.split_into_trigrams()
            checked_trigrams = list()
            important_trigrams = list()

            for trigram in self.trigrams:
                if trigram not in checked_trigrams:
                    this_doc_trigram = self.trigrams.count(trigram)
                    trigram_weight = this_doc_trigram * self.count_ngram_weight(trigram)
                    self.trigrams_weight += trigram_weight
                    checked_trigrams.append(trigram)

                    if trigram_weight:
                        important_trigrams.append(trigram)

            if important_trigrams:
                self.trigrams_weight = self.trigrams_weight / len(important_trigrams)
                logging.info('\nweight by trigrams: %f\n' % self.trigrams_weight)

            else:
                self.trigrams_weight = None
                logging.error('\nimpossible to count weight by trigrams\n')

    def read_training_data(self):
        try:
            if cwd.endswith('master'):
                data = pandas.read_csv(path.join('..', 'databases', 'dataset.csv'), sep=';', encoding='utf-8')

            elif cwd.endswith('dist'):
                data = pandas.read_csv(path.join('..', '..', 'databases', 'dataset.csv'), sep=';', encoding='utf-8')

        except FileNotFoundError or FileExistsError:
            logging.error('\nerror when trying to read training data\n')
            return None

        self.training_data['features'] = data.loc()[:, ['unigrams_weight']]
        self.training_data['labels'] = data['tonal']
        logging.info('\ntraining data was successfully read\n')

    def classification(self):
        try:
            # self.classifier.fit(self.training_data['features'], self.training_data['labels'])
            if os.getcwd().endswith('master'):
                self.classifier = joblib.load(path.join('..', 'databases', 'models', 'model_unigrams.pkl'))

            elif os.getcwd().endswith('dist'):
                self.classifier = joblib.load(path.join('..', '..', 'databases', 'models', 'model_unigrams.pkl'))

        except FileNotFoundError or FileExistsError:
            logging.error('\nmodel for classifier lost\n')
            return None

        if self.unigrams_weight:
            self.tonal = self.classifier.predict(self.unigrams_weight)[0]
            self.probability = max(self.classifier.predict_proba(self.unigrams_weight)[0])
            logging.info("\ndocument's tonal: %s\n" % self.tonal)

        else:
            self.tonal = 'Unknown'

    def count_tonal(self):
        if not self.text:
            self.tonal = 'Unknown'
            return None

        self.count_weight_by_unigrams()
        self.count_weight_by_bigrams()
        self.count_weight_by_trigrams()

        self.unigrams_tf_idf_count()
        self.bigrams_tf_idf_count()
        self.trigrams_tf_idf_count()

        self.classification()
