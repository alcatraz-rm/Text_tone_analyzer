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

import csv
import time
from threading import Thread

from Python.Services.Classifier import Classifier
from Python.Services.Configurator import Configurator
from Python.Services.DatabaseCursor import DatabaseCursor
from Python.Services.DocumentPreparer import DocumentPreparer
from Python.Services.Lemmatizer.Lemmatizer import Lemmatizer
from Python.Services.Logger import Logger
from Python.Services.PathService import PathService
from Python.Services.TextWeightCounter import TextWeightCounter

# TODO: Add text processing with TF-IDF
# TODO: Clean databases
# TODO: Fix bugs speech recognizing
# TODO: Self-learning
# TODO: Maybe, we can work without databases?
# TODO: Add unigrams, bigrams and trigrams tonalities as features and fit main classifier


class TextTonalAnalyzer:
    def __init__(self, classifier_name='NBC'):
        # Services
        self._configurator = Configurator()
        self._configurator.configure_system()

        self._database_cursor = DatabaseCursor()
        self._document_preparer = DocumentPreparer()
        self._text_weight_counter = TextWeightCounter()
        self._classifier = Classifier()
        self.__logger = Logger()
        self._lemmatizer = Lemmatizer()
        self._path_service = PathService()

        # Data
        self._classifier_name = classifier_name

        self._text = None
        self.tonal = None
        self.probability = 0

        self._unigrams = None
        self._bigrams = None
        self._trigrams = None

        self._unigrams_weight = None
        self._bigrams_weight = None
        self._trigrams_weight = None

        self.__logger.info('TextTonalAnalyzer was successfully initialized.', __name__)

    def _reset_data(self):
        self._text = None
        self.tonal = None
        self.probability = 0

        self._unigrams = None
        self._bigrams = None
        self._trigrams = None

        self._unigrams_weight = None
        self._bigrams_weight = None
        self._trigrams_weight = None

        self.__logger.info('Data was successfully reset.', __name__)

    def _document_prepare(self):
        self._unigrams = self._document_preparer.split_into_unigrams(self._text)
        self._bigrams = self._document_preparer.split_into_bigrams(self._text)
        self._trigrams = self._document_preparer.split_into_trigrams(self._text)

    def _text_in_dataset(self):
        path_to_dataset = self._path_service.get_path_to_dataset('dataset_with_unigrams.csv')

        with open(path_to_dataset, 'r', encoding='utf-8') as file:
            dataset = csv.reader(file)
            for doc in dataset:
                doc = ''.join(doc).split(';')
                if doc[0] == self._text:
                    self.tonal = doc[1]
                    self.probability = 1

                    self.__logger.info('Document is in dataset.', __name__)
                    return True

        return False

    def _count_weight_by_unigrams(self):
        self._unigrams_weight = self._text_weight_counter.count_weight_by_unigrams(self._unigrams)

    def _count_weight_by_bigrams(self):
        self._bigrams_weight = self._text_weight_counter.count_weight_by_bigrams(self._bigrams)

    def _count_weight_by_trigrams(self):
        self._trigrams_weight = self._text_weight_counter.count_weight_by_trigrams(self._trigrams)

    def detect_tonal(self, text):
        self._reset_data()

        self._text = self._lemmatizer.get_text_initial_form(text)

        if not self._text:
            self.tonal = 'Unknown'

            self.__logger.warning('Text is empty.', __name__)
            return None

        self._document_prepare()
        # self._vectorizer.vectorize(self.text)

        if not self._text_in_dataset():
            threads = list()

            threads.append(Thread(target=self._count_weight_by_unigrams, args=()))
            threads.append(Thread(target=self._count_weight_by_bigrams, args=()))
            threads.append(Thread(target=self._count_weight_by_trigrams, args=()))

            for thread in threads:
                thread.start()

            for thread in threads:
                while thread.is_alive():
                    time.sleep(0.1)

                thread.join()

            self._classifier.customize(self._unigrams_weight, self._bigrams_weight,
                                       self._trigrams_weight, self._classifier_name)

            self.tonal, self.probability = self._classifier.predict_tonal()

            self.__logger.page_break()
