# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

from sklearn.externals import joblib

from Python.Services.DatabaseCursor import DatabaseCursor
from Python.Services.Lemmatizer.Lemmatizer import Lemmatizer
from Python.Services.DocumentPreparer import DocumentPreparer
from Python.Services.TextWeightCounter import TextWeightCounter

import os
from os import path
import csv


class Document:
    def __init__(self, text, vec_model=None, lemmatized=False):
        if not lemmatized:
            self.text = Lemmatizer().lead_to_initial_form(text)
        else:
            self.text = text

        self.database_cursor = DatabaseCursor()
        self.document_preparer = DocumentPreparer()
        self.text_weight_counter = TextWeightCounter()

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

        self.check_text_in_dataset()

    def check_text_in_dataset(self):
        with open(os.path.join('..', '..', 'Databases', 'dataset_with_unigrams.csv'), 'r', encoding='utf-8') as file:
            dataset = csv.reader(file)
            for doc in dataset:
                doc = ''.join(doc).split(';')
                if doc[0] == self.text:
                    self.tonal = doc[1]
                    self.probability = 1
                    return True

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

        if not self.check_text_in_dataset():
            self.unigrams_weight = self.text_weight_counter.count_weight_by_unigrams(self.unigrams)
            self.bigrams_weight = self.text_weight_counter.count_weight_by_bigrams(self.bigrams)
            self.trigrams_weight = self.text_weight_counter.count_weight_by_trigrams(self.trigrams)

            self.classification()
