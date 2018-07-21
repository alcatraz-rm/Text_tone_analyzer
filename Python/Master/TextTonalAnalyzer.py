# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import os
import csv
import sys
sys.path.append(os.path.join('..', '..'))

from Python.Services.DatabaseCursor import DatabaseCursor
from Python.Services.Lemmatizer.Lemmatizer import Lemmatizer
from Python.Services.DocumentPreparer import DocumentPreparer
from Python.Services.TextWeightCounter import TextWeightCounter
from Python.Services.Classifier import Classifier
from Python.Services.Logger import Logger


class TextTonalAnalyzer:
    def __init__(self):
        # Services
        self.database_cursor = DatabaseCursor()
        self.document_preparer = DocumentPreparer()
        self.text_weight_counter = TextWeightCounter()
        self.classifier = Classifier()
        self.logger = Logger()
        self.lemmatizer = Lemmatizer()

        if not self.logger.configured:
            self.logger.configure()

        # Data
        self.text = None
        self.tonal = None
        self.probability = 0

        self.unigrams = None
        self.bigrams = None
        self.trigrams = None

        self.unigrams_weight = 0
        self.bigrams_weight = 0
        self.trigrams_weight = 0

        self.logger.info('TextTonalAnalyzer was successfully initialized.', 'TextTonalAnalyzer.__init__()')

    def reset_data(self):
        self.text = None
        self.tonal = None
        self.probability = 0

        self.unigrams = None
        self.bigrams = None
        self.trigrams = None

        self.unigrams_weight = 0
        self.bigrams_weight = 0
        self.trigrams_weight = 0

        self.logger.info('Data was successfully reset.', 'TextTonalAnalyzer.reset_data()')

    def document_prepare(self):
        self.unigrams = self.document_preparer.split_into_unigrams(self.text)
        self.bigrams = self.document_preparer.split_into_bigrams(self.text)
        self.trigrams = self.document_preparer.split_into_trigrams(self.text)

    def check_text_in_dataset(self):
        with open(os.path.join('..', '..', 'Databases', 'dataset_with_unigrams.csv'), 'r', encoding='utf-8') as file:
            dataset = csv.reader(file)
            for doc in dataset:
                doc = ''.join(doc).split(';')
                if doc[0] == self.text:
                    self.tonal = doc[1]
                    self.probability = 1

                    self.logger.info('Document is in dataset.', 'TextTonalAnalyzer.check_text_in_dataset()')
                    return True

        return False

    def detect_tonal(self, text):
        self.reset_data()

        self.text = self.lemmatizer.lead_to_initial_form(text)

        if not self.text:
            self.tonal = 'Unknown'

            self.logger.warning('Text is empty.', 'TextTonalAnalyzer.detect_tonal()')
            return None

        self.document_prepare()

        if not self.check_text_in_dataset():
            self.unigrams_weight = self.text_weight_counter.count_weight_by_unigrams(self.unigrams)
            self.bigrams_weight = self.text_weight_counter.count_weight_by_bigrams(self.bigrams)
            self.trigrams_weight = self.text_weight_counter.count_weight_by_trigrams(self.trigrams)

            self.classifier.configure('NBC', self.unigrams_weight, self.bigrams_weight, self.trigrams_weight)
            self.tonal, self.probability = self.classifier.predict()
            self.logger.page_break()
