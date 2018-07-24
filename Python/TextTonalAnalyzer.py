# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import os
import csv
from Python.Services.DatabaseCursor import DatabaseCursor
from Python.Services.Lemmatizer.Lemmatizer import Lemmatizer
from Python.Services.DocumentPreparer import DocumentPreparer
from Python.Services.TextWeightCounter import TextWeightCounter
from Python.Services.Classifier import Classifier
from Python.Services.Logger import Logger


class TextTonalAnalyzer:
    def __init__(self):
        # Services
        self._database_cursor = DatabaseCursor()
        self._document_preparer = DocumentPreparer()
        self._text_weight_counter = TextWeightCounter()
        self._classifier = Classifier()
        self.__logger = Logger()
        self._lemmatizer = Lemmatizer()

        if not self.__logger.configured:
            self.__logger.configure()

        # Data
        self._text = None
        self.tonal = None
        self.probability = 0

        self._unigrams = None
        self._bigrams = None
        self._trigrams = None

        self._unigrams_weight = 0
        self._bigrams_weight = 0
        self._trigrams_weight = 0

        self.__logger.info('TextTonalAnalyzer was successfully initialized.', 'TextTonalAnalyzer.__init__()')

    def _reset_data(self):
        self._text = None
        self.tonal = None
        self.probability = 0

        self._unigrams = None
        self._bigrams = None
        self._trigrams = None

        self._unigrams_weight = 0
        self._bigrams_weight = 0
        self._trigrams_weight = 0

        self.__logger.info('Data was successfully reset.', 'TextTonalAnalyzer._reset_data()')

    def _document_prepare(self):
        self._unigrams = self._document_preparer.split_into_unigrams(self._text)
        self._bigrams = self._document_preparer.split_into_bigrams(self._text)
        self._trigrams = self._document_preparer.split_into_trigrams(self._text)

    def _check_text_in_dataset(self):
        path_to_dataset = None

        if os.getcwd().endswith('Python'):
            path_to_dataset = os.path.join('..', 'Databases', 'dataset_with_unigrams.csv')

        elif os.getcwd().endswith('Tests'):
            path_to_dataset = os.path.join('..', '..', 'Databases', 'dataset_with_unigrams.csv')

        with open(path_to_dataset, 'r', encoding='utf-8') as file:
            dataset = csv.reader(file)
            for doc in dataset:
                doc = ''.join(doc).split(';')
                if doc[0] == self._text:
                    self.tonal = doc[1]
                    self.probability = 1

                    self.__logger.info('Document is in dataset.', 'TextTonalAnalyzer._check_text_in_dataset()')
                    return True

        return False

    def detect_tonal(self, text):
        self._reset_data()

        self._text = self._lemmatizer.lead_to_initial_form(text)

        if not self._text:
            self.tonal = 'Unknown'

            self.__logger.warning('Text is empty.', 'TextTonalAnalyzer.detect_tonal()')
            return None

        self._document_prepare()

        if not self._check_text_in_dataset():
            self._unigrams_weight = self._text_weight_counter.count_weight_by_unigrams(self._unigrams)
            self._bigrams_weight = self._text_weight_counter.count_weight_by_bigrams(self._bigrams)
            self._trigrams_weight = self._text_weight_counter.count_weight_by_trigrams(self._trigrams)

            self._classifier.configure('DecisionTree', self._unigrams_weight, self._bigrams_weight, self._trigrams_weight)
            self.tonal, self.probability = self._classifier.predict()
            self.__logger.page_break()
