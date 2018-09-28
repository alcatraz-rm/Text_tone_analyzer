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

import json
import os
import time
from threading import Thread

from sklearn.externals import joblib

from Python.Services.Containers.ClassificationDataContainer import ClassificationDataContainer
from Python.Services.Logger import Logger
from Python.Services.PathService import PathService


class Classifier:
    def __init__(self):
        # Services
        self.__logger = Logger()

        self._path_service = PathService()

        # Data
        self._container = ClassificationDataContainer()

        self._possible_classifiers = ['NBC', 'LogisticRegression', 'KNN']

        self.__logger.info('Classifier was successfully initialized.', 'Classifier.__init__()')

    def _load_config(self):
        path_to_config = os.path.join(self._path_service.path_to_configs, 'classifier.json')

        with open(path_to_config, 'r', encoding='utf-8') as file:
            config = json.load(file)

        self._possible_classifiers = config['possible_classifiers']

    def configure(self, unigrams_weight, bigrams_weight, trigrams_weight, classifier_name='NBC'):
        self._container.reset()

        if classifier_name in self._possible_classifiers:
            self._container.classifiers['name'] = classifier_name
        else:
            self._container.classifiers['name'] = 'NBC'
            self.__logger.error('Got unknown classifier, set default (NBC).',
                                'Classifier.configure()')

        self._container.weights['unigrams'] = unigrams_weight
        self._container.weights['bigrams'] = bigrams_weight
        self._container.weights['trigrams'] = trigrams_weight

        try:
            if self._container.weights['unigrams']:
                self._container.classifiers['unigrams'] = joblib.load(
                                    self._path_service.get_path_to_model('unigrams',
                                                                         self._container.classifiers['name']))

            if self._container.weights['bigrams']:
                self._container.classifiers['bigrams'] = joblib.load(
                                    self._path_service.get_path_to_model('bigrams',
                                                                         self._container.classifiers['name']))

            if self._container.weights['trigrams']:
                self._container.classifiers['trigrams'] = joblib.load(
                                    self._path_service.get_path_to_model('trigrams',
                                                                         self._container.classifiers['name']))

            self.__logger.info('Models were successfully loaded.', 'Classifier.configure()')
            self.__logger.info('Classifier was successfully configured.', 'Classifier.configure()')

        except FileNotFoundError or FileExistsError:
            self.__logger.fatal(f'File not found: {str(FileNotFoundError.filename)}', 'Classifier.configure()')

    def _predict_unigrams(self):
        self._container.tonalities['unigrams'] = self._container.classifiers['unigrams'].predict(
                                                                        self._container.weights['unigrams'])[0]

        self._container.probabilities['unigrams'] = max(self._container.classifiers['unigrams'].predict_proba(
                                                                        self._container.weights['unigrams'])[0])

        self.__logger.info(f'Unigrams tonal: {self._container.tonalities["unigrams"]}', 'Classifier.predict()')
        self.__logger.info(f'Unigrams probability: {self._container.probabilities["unigrams"]}', 'Classifier.predict()')

    def _predict_bigrams(self):
        self._container.tonalities['bigrams'] = self._container.classifiers['bigrams'].predict(
                                                                                  [[self._container.weights['unigrams'],
                                                                                    self._container.weights['bigrams']]]
                                                                                                                    )[0]

        self._container.probabilities['bigrams'] = max(self._container.classifiers['bigrams'].predict_proba([[
                                                                                 self._container.weights['unigrams'],
                                                                                 self._container.weights['bigrams']]]
                                                                                                                )[0])

        self.__logger.info(f'Bigrams tonal: {self._container.tonalities["bigrams"]}', 'Classifier.predict()')
        self.__logger.info(f'Bigrams probability: {self._container.probabilities["bigrams"]}', 'Classifier.predict()')

    def _predict_trigrams(self):
        self._container.tonalities['trigrams'] = self._container.classifiers['trigrams'].predict([[
                                                                             self._container.weights['unigrams'],
                                                                             self._container.weights['bigrams'],
                                                                             self._container.weights['trigrams']]])[0]

        self._container.probabilities['trigrams'] = max(self._container.classifiers['trigrams'].predict_proba([[
                                                                                   self._container.weights['unigrams'],
                                                                                   self._container.weights['bigrams'],
                                                                                   self._container.weights['trigrams']]]
                                                                                                                   )[0])

        self.__logger.info(f'Trigrams tonal: {self._container.tonalities["trigrams"]}', 'Classifier.predict()')
        self.__logger.info(f'Trigrams probability: {self._container.probabilities["trigrams"]}', 'Classifier.predict()')

    def predict(self):
        threads = list()

        if self._container.weights['unigrams']:
            threads.append(Thread(target=self._predict_unigrams, args=()))

        if self._container.weights['bigrams']:
            threads.append(Thread(target=self._predict_bigrams, args=()))

        if self._container.weights['trigrams']:
            threads.append(Thread(target=self._predict_trigrams, args=()))

        for thread in threads:
            thread.start()

        for thread in threads:
            while thread.is_alive():
                time.sleep(0.1)

            thread.join()

        if self._container.tonalities['unigrams'] and self._container.tonalities['bigrams'] and \
                self._container.tonalities['trigrams']:

            if self._container.tonalities['unigrams'] == self._container.tonalities['bigrams']:
                self._container.tonalities['final'] = self._container.tonalities['unigrams']
                self._container.probabilities['final'] = max(self._container.probabilities['unigrams'],
                                                             self._container.probabilities['bigrams'])

            elif self._container.tonalities['unigrams'] == self._container.tonalities['trigrams']:
                self._container.tonalities['final'] = self._container.tonalities['unigrams']
                self._container.probabilities['final'] = max(self._container.probabilities['unigrams'],
                                                             self._container.probabilities['trigrams'])

            elif self._container.tonalities['bigrams'] == self._container.tonalities['trigrams']:
                self._container.tonalities['final'] = self._container.tonalities['bigrams']
                self._container.probabilities['final'] = max(self._container.probabilities['bigrams'],
                                                             self._container.probabilities['trigrams'])

        elif self._container.tonalities['unigrams'] and self._container.tonalities['bigrams']:

            if self._container.tonalities['unigrams'] != self._container.tonalities['bigrams']:
                if self._container.probabilities['unigrams'] >= self._container.probabilities['bigrams']:
                    self._container.tonalities['final'] = self._container.tonalities['unigrams']
                    self._container.probabilities['final'] = self._container.probabilities['unigrams']

                else:
                    self._container.tonalities['final'] = self._container.tonalities['bigrams']
                    self._container.probabilities['final'] = self._container.probabilities['bigrams']

            elif self._container.tonalities['unigrams'] == self._container.tonalities['bigrams']:
                    self._container.tonalities['final'] = self._container.tonalities['unigrams']
                    self._container.probabilities['final'] = max(self._container.probabilities['bigrams'],
                                                                 self._container.probabilities['unigrams'])

        elif self._container.tonalities['unigrams']:
            self._container.tonalities['final'] = self._container.tonalities['unigrams']
            self._container.probabilities['final'] = self._container.probabilities['unigrams']

        self.__logger.info(f'Final tonal: {self._container.tonalities["final"]}', 'Classifier.predict()')
        self.__logger.info(f'Final probability: {self._container.probabilities["final"]}', 'Classifier.predict()')

        return self._container.tonalities['final'], self._container.probabilities['final']
