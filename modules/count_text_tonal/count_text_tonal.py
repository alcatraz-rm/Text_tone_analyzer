# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

from modules.lemmatization.lemmatization import lemmatization
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from modules.get_ngram_info.get_ngram_info import get_ngram_info
import math
import logging
import pandas
import os
from os import path

docs_count = 103582  # hardcode
cwd = os.getcwd()


class Document:
    def __init__(self, text, vec_model=None):
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
        self.unigrams_tonal = None
        self.bigrams_tonal = None
        self.trigrams_tonal = None
        self.unigrams_probability = None
        self.bigrams_probability = None
        self.trigrams_probability = None
        self.tonal = None
        self.vec_model = vec_model
        self.probability = None
        self.unigrams_classifier = None
        self.bigrams_classifier = None
        self.trigrams_classifier = None
        self.classifier_name = 'nbc'
        self.unigrams_tf_idf = dict()
        self.bigrams_tf_idf = dict()
        self.trigrams_tf_idf = dict()

        if len(self.unigrams) >= 2:
            self.split_into_bigrams()
        if len(self.unigrams) >= 3:
            self.split_into_trigrams()

        try:
            if self.unigrams:
                self.unigrams_classifier = joblib.load(path.join('..', 'databases', 'models', self.classifier_name, 'model_unigrams.pkl'))

            if self.bigrams:
                self.bigrams_classifier = joblib.load(path.join('..', 'databases', 'models', self.classifier_name, 'model_bigrams.pkl'))

            if self.trigrams:
                self.trigrams_classifier = joblib.load(path.join('..', 'databases', 'models', self.classifier_name, 'model_trigrams.pkl'))

        except FileNotFoundError or FileExistsError:
            logging.error('\nmodel for classifier lost\n')

        # self.unigrams_tf_idf_count()
        # self.bigrams_tf_idf_count()
        # self.trigrams_tf_idf_count()

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

    def count_ngram_weight(self, ngram, mode):
        if mode == 1:
            pos_docs = 48179  # hardcode
            neg_docs = 65403  # hardcode
            pos_docs_word, neg_docs_word, neu_docs_word = get_ngram_info(ngram, self.vec_model)

            if (not (pos_docs_word and neg_docs_word)) or (pos_docs_word == 1 and neg_docs_word == 1):
                return 0

            delta_tf_idf = math.log10((neg_docs * pos_docs_word) / (pos_docs * neg_docs_word))
            logging.info('\nN-gram, delta TF-IDF (mode 1): %s, %f\n' % (ngram, delta_tf_idf))

        elif mode == 2:
            non_neu_docs = 30000  # hardcode
            neu_docs = 16896  # hardcode
            pos_docs_word, neg_docs_word, neu_docs_word = get_ngram_info(ngram, self.vec_model)
            non_neu_docs_word = pos_docs_word + neg_docs_word

            if (not (pos_docs_word and neg_docs_word)) or (pos_docs_word == 1 and neg_docs_word == 1):
                return 0

            delta_tf_idf = math.log10((neu_docs * non_neu_docs_word) / (non_neu_docs * neu_docs_word))
            logging.info('\nN-gram, delta TF-IDF (mode 2): %s, %f\n' % (ngram, delta_tf_idf))

        else:
            delta_tf_idf = 0
            logging.info('\nGet incorrect mode\n')

        return delta_tf_idf

    def count_weight_by_unigrams_tf_idf(self):
        checked_unigrams = list()
        important_unigrams = list()

        for unigram in self.unigrams:
            if unigram not in checked_unigrams:
                unigram_weight = self.unigrams_tf_idf[unigram] * self.count_ngram_weight(unigram, mode=1)
                self.unigrams_weight_tf_idf += unigram_weight
                checked_unigrams.append(unigram)

                if unigram_weight:
                    important_unigrams.append(unigram)

        if len(important_unigrams) >= round(len(self.unigrams) * 0.6) and important_unigrams:
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
                unigram_weight = this_doc_unigram * self.count_ngram_weight(unigram, mode=1)
                self.unigrams_weight += unigram_weight
                checked_unigrams.append(unigram)

                if unigram_weight:
                    important_unigrams.append(unigram)

        if len(important_unigrams) >= round(len(self.unigrams) * 0.6) and important_unigrams:
            self.unigrams_weight = self.unigrams_weight / len(important_unigrams)
            logging.info('\nweight by unigrams: %f\n' % self.unigrams_weight)

        else:
            self.unigrams_weight = None
            logging.error('\nimpossible to count weight by unigrams\n')

    def count_weight_by_bigrams_tf_idf(self):
        if len(self.unigrams) >= 2:
            checked_bigrams = list()
            important_bigrams = list()

            for bigram in self.bigrams:
                if bigram not in checked_bigrams:
                    bigram_weight = self.bigrams_tf_idf[bigram] * self.count_ngram_weight(bigram, mode=1)
                    self.bigrams_weight_tf_idf += bigram_weight
                    checked_bigrams.append(bigram)

                    if bigram_weight:
                        important_bigrams.append(bigram)

            if len(important_bigrams) >= len(self.bigrams) // 2 and important_bigrams:
                self.bigrams_weight_tf_idf = self.bigrams_weight_tf_idf / len(important_bigrams)
                logging.info('\nweight by bigrams with TF-IDF: %f\n' % self.bigrams_weight_tf_idf)

            else:
                self.bigrams_weight_tf_idf = None
                logging.error('\nimpossible to count weight by bigrams with TF-IDF\n')

    def count_weight_by_bigrams(self):
        if len(self.unigrams) >= 2:
            checked_bigrams = list()
            important_bigrams = list()

            for bigram in self.bigrams:
                if bigram not in checked_bigrams:
                    this_doc_bigram = self.bigrams.count(bigram)
                    bigram_weight = this_doc_bigram * self.count_ngram_weight(bigram, mode=1)
                    self.bigrams_weight += bigram_weight
                    checked_bigrams.append(bigram)

                    if bigram_weight:
                        important_bigrams.append(bigram)

            if len(important_bigrams) >= len(self.bigrams) // 2 and important_bigrams:
                self.bigrams_weight = self.bigrams_weight / len(important_bigrams)
                logging.info('\nweight by bigrams: %f\n' % self.bigrams_weight)

            else:
                self.bigrams_weight = None
                logging.error('\nimpossible to count weight by bigrams\n')

    def count_weight_by_trigrams_tf_idf(self):
        if len(self.unigrams) >= 3:
            checked_trigrams = list()
            important_trigrams = list()

            for trigram in self.trigrams:
                if trigram not in checked_trigrams:
                    trigram_weight = self.trigrams_tf_idf[trigram] * self.count_ngram_weight(trigram, mode=1)
                    self.trigrams_weight_tf_idf += trigram_weight
                    checked_trigrams.append(trigram)

                    if trigram_weight:
                        important_trigrams.append(trigram)

            if len(important_trigrams) >= round(len(self.trigrams) * 0.4) and important_trigrams:
                self.trigrams_weight_tf_idf = self.trigrams_weight_tf_idf / len(important_trigrams)
                logging.info('\nweight by trigrams with TF-IDF: %f\n' % self.trigrams_weight_tf_idf)

            else:
                self.trigrams_weight_tf_idf = None
                logging.error('\nimpossible to count weight by trigrams with TF-IDF\n ')

    def count_weight_by_trigrams(self):
        if len(self.unigrams) >= 3:
            checked_trigrams = list()
            important_trigrams = list()

            for trigram in self.trigrams:
                if trigram not in checked_trigrams:
                    this_doc_trigram = self.trigrams.count(trigram)
                    trigram_weight = this_doc_trigram * self.count_ngram_weight(trigram, mode=1)
                    self.trigrams_weight += trigram_weight
                    checked_trigrams.append(trigram)

                    if trigram_weight:
                        important_trigrams.append(trigram)

            if len(important_trigrams) >= round(len(self.trigrams) * 0.4) and important_trigrams:
                self.trigrams_weight = self.trigrams_weight / len(important_trigrams)
                logging.info('\nweight by trigrams: %f\n' % self.trigrams_weight)

            else:
                self.trigrams_weight = None
                logging.error('\nimpossible to count weight by trigrams\n')

    def classification(self):
        if self.unigrams_weight:
            self.unigrams_tonal = self.unigrams_classifier.predict(self.unigrams_weight)[0]
            self.unigrams_probability = max(self.unigrams_classifier.predict_proba(self.unigrams_weight)[0])

            logging.info("\ndocument's tonal by unigrams: %s\n" % self.unigrams_tonal)
            logging.info('\nprobability by unigrams: %f\n' % self.unigrams_probability)

        if self.bigrams_weight:
            self.bigrams_tonal = self.bigrams_classifier.predict([[self.unigrams_weight, self.bigrams_weight]])[0]
            self.bigrams_probability = max(self.bigrams_classifier.predict_proba([[self.unigrams_weight, self.bigrams_weight]])[0])

            logging.info("\ndocument's tonal by bigrams: %s\n" % self.bigrams_tonal)
            logging.info('\nprobability by bigrams: %f\n' % self.bigrams_probability)

        if self.trigrams_weight:
            self.trigrams_tonal = self.trigrams_classifier.predict([[self.unigrams_weight, self.bigrams_weight, self.trigrams_weight]])[0]
            self.trigrams_probability = max(self.trigrams_classifier.predict_proba([[self.unigrams_weight, self.bigrams_weight, self.trigrams_weight]])[0])

            logging.info("\ndocument's tonal by trigrams: %s\n" % self.trigrams_tonal)
            logging.info('\nprobability by trigrams: %f\n' % self.trigrams_probability)

        if self.unigrams_tonal and self.bigrams_tonal and self.trigrams_tonal:
            if self.unigrams_tonal == self.bigrams_tonal:
                self.tonal = self.unigrams_tonal
                self.probability = max(self.unigrams_probability, self.bigrams_probability)
            elif self.unigrams_tonal == self.trigrams_tonal:
                self.tonal = self.unigrams_tonal
                self.probability = max(self.unigrams_probability, self.trigrams_probability)
            elif self.bigrams_tonal == self.trigrams_tonal:
                self.tonal = self.bigrams_tonal
                self.probability = max(self.bigrams_probability, self.trigrams_probability)

        if self.unigrams_tonal and self.bigrams_tonal:
            if self.unigrams_tonal != self.bigrams_tonal:
                if self.unigrams_probability >= self.bigrams_probability:
                    self.tonal = self.unigrams_tonal
                    self.probability = self.unigrams_probability
                else:
                    self.tonal = self.bigrams_tonal
                    self.probability = self.bigrams_probability
            else:
                self.tonal = self.unigrams_tonal
                self.probability = max(self.unigrams_probability, self.bigrams_probability)

        elif self.unigrams_tonal:
            self.tonal = self.unigrams_tonal
            self.probability = self.unigrams_probability

        else:
            self.tonal = 'Unknown'

    def count_tonal(self):
        if not self.text:
            self.tonal = 'Unknown'
            return None

        self.count_weight_by_unigrams()
        self.count_weight_by_bigrams()
        self.count_weight_by_trigrams()

        # self.count_weight_by_unigrams_tf_idf()
        # self.count_weight_by_bigrams_tf_idf()
        # self.count_weight_by_trigrams_tf_idf()

        self.classification()
