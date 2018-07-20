# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

from sklearn.externals import joblib

from Python.Services.DatabaseCursor import DatabaseCursor
from Python.Services.Lemmatizer.Lemmatizer import Lemmatizer
from Python.Services.DocumentPreparer import DocumentPreparer
from Python.Services.TextWeightCounter import TextWeightCounter
from Python.Services.Classifier import Classifier

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
        self.classifier = Classifier()

        self.unigrams = self.document_preparer.split_into_unigrams(self.text)
        self.bigrams = self.document_preparer.split_into_bigrams(self.text)
        self.trigrams = self.document_preparer.split_into_trigrams(self.text)

        self.unigrams_weight = 0
        self.unigrams_weight_tf_idf = 0
        self.bigrams_weight = 0
        self.bigrams_weight_tf_idf = 0
        self.trigrams_weight = 0
        self.trigrams_weight_tf_idf = 0
        self.vec_model = vec_model
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

    def count_tonal(self):
        if not self.text:
            self.tonal = 'Unknown'
            return None

        if not self.check_text_in_dataset():
            self.unigrams_weight = self.text_weight_counter.count_weight_by_unigrams(self.unigrams)
            self.bigrams_weight = self.text_weight_counter.count_weight_by_bigrams(self.bigrams)
            self.trigrams_weight = self.text_weight_counter.count_weight_by_trigrams(self.trigrams)

            self.classifier.configure('NBC', self.unigrams_weight, self.bigrams_weight, self.trigrams_weight)
            self.tonal, self.probability = self.classifier.predict()
