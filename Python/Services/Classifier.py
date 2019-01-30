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

import time
from threading import Thread

from sklearn.externals import joblib

from Python.Services.Containers.ClassificationDataContainer import ClassificationDataContainer
from Python.Services.Logger import Logger
from Python.Services.PathService import PathService
from Python.Services.ExceptionsHandler import ExceptionsHandler


class Classifier:
    def __init__(self):
        # Services
        self.__logger = Logger()
        self._path_service = PathService()
        self._exceptions_handler = ExceptionsHandler()

        # Data
        self._container = ClassificationDataContainer()
        self._possible_classifiers = ['NBC', 'LogisticRegression', 'KNN', 'RandomForest']

        self.__logger.info('Classifier was successfully initialized.', __name__)

    def customize(self, unigrams_weight: float, bigrams_weight: float,
                  trigrams_weight: float, classifier_name='NBC'):
        self._container.clear()

        if classifier_name in self._possible_classifiers:
            self._container.classifiers['name'] = classifier_name
        else:
            self._container.classifiers['name'] = 'NBC'
            self.__logger.error('Got unknown classifier, set default (NBC).', __name__)

        self._container.weights['unigrams'] = unigrams_weight
        self._container.weights['bigrams'] = bigrams_weight
        self._container.weights['trigrams'] = trigrams_weight

        try:
            if self._container.weights['unigrams']:
                self._container.classifiers['unigrams'] = joblib.load(
                    self._path_service.get_path_to_model('unigrams', self._container.classifiers['name']))

            if self._container.weights['bigrams']:
                self._container.classifiers['bigrams'] = joblib.load(
                    self._path_service.get_path_to_model('bigrams', self._container.classifiers['name']))

            if self._container.weights['trigrams']:
                self._container.classifiers['trigrams'] = joblib.load(
                    self._path_service.get_path_to_model('trigrams', self._container.classifiers['name']))

            self.__logger.info('Models were successfully loaded.', __name__)
            self.__logger.info('Classifier was successfully configured.', __name__)

        except BaseException as exception:
            self.__logger.fatal(self._exceptions_handler.get_error_message(exception), __name__)

    def _predict_tonal_by_unigrams(self):
        self._container.tonalities['unigrams'] = self._container.classifiers['unigrams'].predict([[
            self._container.weights['unigrams']]])[0]

        self._container.probabilities['unigrams'] = max(self._container.classifiers['unigrams'].predict_proba([[
            self._container.weights['unigrams']]])[0])

        self.__logger.info(f'Unigrams tonal: {self._container.tonalities["unigrams"]}', __name__)
        self.__logger.info(f'Unigrams probability: {self._container.probabilities["unigrams"]}', __name__)

    def _predict_tonal_by_unigrams_bigrams(self):
        self._container.tonalities['bigrams'] = self._container.classifiers['bigrams'].predict(
            [[self._container.weights['unigrams'],
              self._container.weights['bigrams']]]
        )[0]

        self._container.probabilities['bigrams'] = max(self._container.classifiers['bigrams'].predict_proba([[
            self._container.weights['unigrams'],
            self._container.weights['bigrams']]]
        )[0])

        self.__logger.info(f'Bigrams tonal: {self._container.tonalities["bigrams"]}', __name__)
        self.__logger.info(f'Bigrams probability: {self._container.probabilities["bigrams"]}', __name__)

    def _predict_tonal_by_unigrams_bigrams_trigrams(self):
        self._container.tonalities['trigrams'] = self._container.classifiers['trigrams'].predict([[
            self._container.weights['unigrams'],
            self._container.weights['bigrams'],
            self._container.weights['trigrams']]])[0]

        self._container.probabilities['trigrams'] = max(self._container.classifiers['trigrams'].predict_proba([[
            self._container.weights['unigrams'],
            self._container.weights['bigrams'],
            self._container.weights['trigrams']]]
        )[0])

        self.__logger.info(f'Trigrams tonal: {self._container.tonalities["trigrams"]}', __name__)
        self.__logger.info(f'Trigrams probability: {self._container.probabilities["trigrams"]}', __name__)

    def _predict_intermediate_tonalities(self):
        threads = list()

        if self._container.weights['unigrams']:
            threads.append(Thread(target=self._predict_tonal_by_unigrams, args=()))

        if self._container.weights['bigrams']:
            threads.append(Thread(target=self._predict_tonal_by_unigrams_bigrams, args=()))

        if self._container.weights['trigrams']:
            threads.append(Thread(target=self._predict_tonal_by_unigrams_bigrams_trigrams, args=()))

        for thread in threads:
            thread.start()

        for thread in threads:
            while thread.is_alive():
                time.sleep(0.1)

            thread.join()

    def _select_final_tonal(self):
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

    def predict_tonal(self):
        self._predict_intermediate_tonalities()
        self._select_final_tonal()

        self.__logger.info(f'Final tonal: {self._container.tonalities["final"]}', __name__)
        self.__logger.info(f'Final probability: {self._container.probabilities["final"]}', __name__)

        return self._container.tonalities['final'], self._container.probabilities['final']

    def __del__(self):
        del self._path_service
        del self._container
        del self._exceptions_handler
        del self._possible_classifiers
        del self.__logger
