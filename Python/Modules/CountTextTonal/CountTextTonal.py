# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

from sklearn.externals import joblib
from Python.Services.DatabaseCursor import DatabaseCursor
from Python.Services.Lemmatizer.Lemmatizer import Lemmatizer
from Python.Services.DocumentPreparer import DocumentPreparer

import math
import os
from os import path
import csv


def count_docs(mode):
    with open(os.path.join('..', '..', 'Databases', 'dataset_with_%s.csv' % mode), 'r', encoding='utf-8') as file:
        pos = 0
        neg = 10000  # magic number, but results are better
        for row in csv.reader(file):
            if ''.join(row).split(';')[1] == 'positive':
                pos += 1
            else:
                neg += 1

    return pos + neg - 10000, pos, neg


# method for counting all docs
unigrams_docs_count, unigrams_pos_docs, unigrams_neg_docs = count_docs('unigrams')
bigrams_docs_count, bigrams_pos_docs, bigrams_neg_docs = count_docs('bigrams')
trigrams_docs_count, trigrams_pos_docs, trigrams_neg_docs = count_docs('trigrams')
cwd = os.getcwd()


class Document:
    # split this class on other classes
    def __init__(self, text, vec_model=None, lemmatized=False):
        # Don't do it in constructor
        if not lemmatized:
            self.text = Lemmatizer().lead_to_initial_form(text)
        else:
            self.text = text

        self.database_cursor = DatabaseCursor()
        self.document_preparer = DocumentPreparer()

        self.unigrams = self.document_preparer.split_into_unigrams(self.text)
        self.bigrams = self.document_preparer.split_into_bigrams(self.text)
        self.trigrams = self.document_preparer.split_into_trigrams(self.text)

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
        self.classifier_name = 'NBC'
        self.unigrams_tf_idf = dict()
        self.bigrams_tf_idf = dict()
        self.trigrams_tf_idf = dict()
        self.text_in_dataset = False

        # Don't do this here
        self.check_text_in_dataset()

    def check_text_in_dataset(self):
        with open(os.path.join('..', '..', 'Databases', 'dataset_with_unigrams.csv'), 'r', encoding='utf-8') as file:
            dataset = csv.reader(file)
            for doc in dataset:
                doc = ''.join(doc).split(';')
                if doc[0] == self.text:
                    self.text_in_dataset = True
                    self.tonal = doc[1]
                    self.probability = 1
                    break

    # class WeightCounter
    def count_ngram_weight(self, ngram):
        pos_docs = None
        neg_docs = None

        if ngram.count(' ') == 0:
            pos_docs = unigrams_pos_docs
            neg_docs = unigrams_neg_docs
        elif ngram.count(' ') == 1:
            pos_docs = unigrams_pos_docs
            neg_docs = unigrams_neg_docs
        elif ngram.count(' ') == 2:
            pos_docs = unigrams_pos_docs
            neg_docs = unigrams_neg_docs

        pos_docs_word, neg_docs_word, neu_docs_word = self.database_cursor.get_info(ngram)

        if (not (pos_docs_word and neg_docs_word)) or (pos_docs_word == 1 and neg_docs_word == 1):
            return 0

        delta_tf_idf = math.log10((neg_docs * pos_docs_word) / (pos_docs * neg_docs_word))

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

        if len(important_unigrams) >= round(len(self.unigrams) * 0.6) and important_unigrams:
            self.unigrams_weight_tf_idf = self.unigrams_weight_tf_idf / len(important_unigrams)

        else:
            self.unigrams_weight_tf_idf = None

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

        if len(important_unigrams) >= round(len(self.unigrams) * 0.6) and important_unigrams:
            self.unigrams_weight = self.unigrams_weight / len(important_unigrams)

        else:
            self.unigrams_weight = None

    def count_weight_by_bigrams_tf_idf(self):
        if len(self.unigrams) >= 2:
            checked_bigrams = list()
            important_bigrams = list()

            for bigram in self.bigrams:
                if bigram not in checked_bigrams:
                    bigram_weight = self.bigrams_tf_idf[bigram] * self.count_ngram_weight(bigram)
                    self.bigrams_weight_tf_idf += bigram_weight
                    checked_bigrams.append(bigram)

                    if bigram_weight:
                        important_bigrams.append(bigram)

            if len(important_bigrams) >= len(self.bigrams) // 2 and important_bigrams:
                self.bigrams_weight_tf_idf = self.bigrams_weight_tf_idf / len(important_bigrams)

            else:
                self.bigrams_weight_tf_idf = None

    def count_weight_by_bigrams(self):
        if len(self.unigrams) >= 2:
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

            if len(important_bigrams) >= len(self.bigrams) // 2 and important_bigrams:
                self.bigrams_weight = self.bigrams_weight / len(important_bigrams)

            else:
                self.bigrams_weight = None

    def count_weight_by_trigrams_tf_idf(self):
        if len(self.unigrams) >= 3:
            checked_trigrams = list()
            important_trigrams = list()

            for trigram in self.trigrams:
                if trigram not in checked_trigrams:
                    trigram_weight = self.trigrams_tf_idf[trigram] * self.count_ngram_weight(trigram)
                    self.trigrams_weight_tf_idf += trigram_weight
                    checked_trigrams.append(trigram)

                    if trigram_weight:
                        important_trigrams.append(trigram)

            if len(important_trigrams) >= round(len(self.trigrams) * 0.4) and important_trigrams:
                self.trigrams_weight_tf_idf = self.trigrams_weight_tf_idf / len(important_trigrams)

            else:
                self.trigrams_weight_tf_idf = None

    def count_weight_by_trigrams(self):
        if len(self.unigrams) >= 3:
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

            if len(important_trigrams) >= round(len(self.trigrams) * 0.4) and important_trigrams:
                self.trigrams_weight = self.trigrams_weight / len(important_trigrams)

            else:
                self.trigrams_weight = None

    # class Classifier
    def classification(self):
        # split into methods
        try:
            if self.unigrams:
                self.unigrams_classifier = joblib.load(path.join('..', '..', 'Databases', 'Models', self.classifier_name, 'model_unigrams.pkl'))

            if self.bigrams:
                self.bigrams_classifier = joblib.load(path.join('..', '..', 'Databases', 'Models', self.classifier_name, 'model_bigrams.pkl'))

            if self.trigrams:
                self.trigrams_classifier = joblib.load(path.join('..', '..', 'Databases', 'Models', self.classifier_name, 'model_trigrams.pkl'))

        except FileNotFoundError or FileExistsError:
            pass
            # logging.error('\nmodel for classifier lost\n')

        if self.unigrams_weight:
            self.unigrams_tonal = self.unigrams_classifier.predict(self.unigrams_weight)[0]
            self.unigrams_probability = max(self.unigrams_classifier.predict_proba(self.unigrams_weight)[0])

        if self.bigrams_weight:
            self.bigrams_tonal = self.bigrams_classifier.predict([[self.unigrams_weight, self.bigrams_weight]])[0]
            self.bigrams_probability = max(self.bigrams_classifier.predict_proba([[self.unigrams_weight, self.bigrams_weight]])[0])

        if self.trigrams_weight:
            self.trigrams_tonal = self.trigrams_classifier.predict([[self.unigrams_weight, self.bigrams_weight, self.trigrams_weight]])[0]
            self.trigrams_probability = max(self.trigrams_classifier.predict_proba([[self.unigrams_weight, self.bigrams_weight, self.trigrams_weight]])[0])

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

        if not self.tonal:
            self.count_weight_by_unigrams()
            self.count_weight_by_bigrams()
            self.count_weight_by_trigrams()

            self.classification()
