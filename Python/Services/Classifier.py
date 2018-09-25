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

import os
import json
from threading import Thread
from sklearn.externals import joblib
from Python.Services.Logger import Logger
from Python.Services.PathService import PathService
from Python.Services.Containers.ClassifierDataContainer import ClassifierDataContainer


class Classifier:
    def __init__(self):
        # Services
        self.__logger = Logger()

        if not self.__logger.configured:
            self.__logger.configure()

        self._path_service = PathService()

        # Data
        self._container = ClassifierDataContainer()
        # self._classifier_name = None
        # self._unigrams_classifier = None
        # self._bigrams_classifier = None
        # self._trigrams_classifier = None
        #
        # self._unigrams_tonal = None
        # self._bigrams_tonal = None
        # self._trigrams_tonal = None
        #
        # self._unigrams_weight = None
        # self._bigrams_weight = None
        # self._trigrams_weight = None
        #
        # self._unigrams_probability = 0
        # self._bigrams_probability = 0
        # self._trigrams_probability = 0

        self._possible_classifiers = ['NBC', 'LogisticRegression', 'KNN']

        # self.tonal = None
        # self.probability = 0

        self.__logger.info('Classifier was successfully initialized.', 'Classifier.__init__()')

    def _load_config(self):
        path_to_config = os.path.join(self._path_service.path_to_configs, 'classifier.json')

        with open(path_to_config, 'r', encoding='utf-8') as file:
            config = json.load(file)

        self._possible_classifiers = config['possible_classifiers']

    def configure(self, unigrams_weight, bigrams_weight, trigrams_weight, classifier_name='NBC'):
        self._container.reset()

        if classifier_name in self._possible_classifiers:
            self._container.classifier_name = classifier_name
        else:
            self._container.classifier_name = 'NBC'
            self.__logger.error('Got unknown classifier, set default (NBC).',
                                'Classifier.configure()')

        # check_spelling that it is number
        self._container.unigrams_weight = unigrams_weight
        self._container.bigrams_weight = bigrams_weight
        self._container.trigrams_weight = trigrams_weight
        #
        # self._container.unigrams_classifier = None
        # self._container.bigrams_classifier = None
        # self._container.trigrams_classifier = None
        #
        # self._container.unigrams_probability = 0
        # self._container.bigrams_probability = 0
        # self._container.trigrams_probability = 0
        #
        # self._container.unigrams_tonal = None
        # self._container.bigrams_tonal = None
        # self._container.trigrams_tonal = None

        try:
            if self._container.unigrams_weight:
                self._container.unigrams_classifier = joblib.load(self._path_service.get_path_to_model('unigrams',
                                                                  self._container.classifier_name))

            if self._container.bigrams_weight:
                self._container.bigrams_classifier = joblib.load(self._path_service.get_path_to_model('bigrams',
                                                                 self._container.classifier_name))

            if self._container.trigrams_weight:
                self._container.trigrams_classifier = joblib.load(self._path_service.get_path_to_model('trigrams',
                                                                  self._container.classifier_name))

            self.__logger.info('Models were successfully loaded.', 'Classifier.configure()')
            self.__logger.info('Classifier was successfully configured.', 'Classifier.configure()')

        except FileNotFoundError or FileExistsError:
            self.__logger.fatal('File not found: %s' % str(FileNotFoundError.filename), 'Classifier.configure()')

    def _predict_unigrams(self):
        self._container.unigrams_tonal = self._container.unigrams_classifier.predict(self._container.unigrams_weight)[0]
        self._container.unigrams_probability = max(self._container.unigrams_classifier.predict_proba(
            self._container.unigrams_weight)[0])

        self.__logger.info('Unigrams tonal: %s' % self._container.unigrams_tonal, 'Classifier.predict()')
        self.__logger.info('Unigrams probability: %f' % self._container.unigrams_probability, 'Classifier.predict()')

    def _predict_bigrams(self):
        self._container.bigrams_tonal = self._container.bigrams_classifier.predict([[self._container.unigrams_weight,
                                                                                     self._container.bigrams_weight]])[0]
        self._container.bigrams_probability = max(self._container.bigrams_classifier.predict_proba([[
                                                                                 self._container.unigrams_weight,
                                                                                 self._container.bigrams_weight]])[0])

        self.__logger.info('Bigrams tonal: %s' % self._container.bigrams_tonal, 'Classifier.predict()')
        self.__logger.info('Bigrams probability: %f' % self._container.bigrams_probability, 'Classifier.predict()')

    def _predict_trigrams(self):
        self._container.trigrams_tonal = self._container.trigrams_classifier.predict([[
                                                                             self._container.unigrams_weight,
                                                                             self._container.bigrams_weight,
                                                                             self._container.trigrams_weight]])[0]
        self._container.trigrams_probability = max(self._container.trigrams_classifier.predict_proba([[
                                                                                   self._container.unigrams_weight,
                                                                                   self._container.bigrams_weight,
                                                                                   self._container.trigrams_weight]])[0])

        self.__logger.info('Trigrams tonal: %s' % self._container.trigrams_tonal, 'Classifier.predict()')
        self.__logger.info('Trigrams probability: %f' % self._container.trigrams_probability, 'Classifier.predict()')

    def predict(self):
        if self._container.unigrams_weight:
            u_thread = Thread(target=self._predict_unigrams, args=())
            u_thread.start()
            u_thread.join()

        if self._container.bigrams_weight:
            b_thread = Thread(target=self._predict_bigrams, args=())
            b_thread.start()
            b_thread.join()

        if self._container.trigrams_weight:
            t_thread = Thread(target=self._predict_trigrams, args=())
            t_thread.start()
            t_thread.join()

        if self._container.unigrams_tonal and self._container.bigrams_tonal and self._container.trigrams_tonal:

            if self._container.unigrams_tonal == self._container.bigrams_tonal:
                self._container.tonal = self._container.unigrams_tonal
                self._container.probability = max(self._container.unigrams_probability,
                                                  self._container.bigrams_probability)

            elif self._container.unigrams_tonal == self._container.trigrams_tonal:
                self._container.tonal = self._container.unigrams_tonal
                self._container.probability = max(self._container.unigrams_probability,
                                                  self._container.trigrams_probability)

            elif self._container.bigrams_tonal == self._container.trigrams_tonal:
                self._container.tonal = self._container.bigrams_tonal
                self._container.probability = max(self._container.bigrams_probability,
                                                  self._container.trigrams_probability)

        elif self._container.unigrams_tonal and self._container.bigrams_tonal:

            if self._container.unigrams_tonal != self._container.bigrams_tonal:
                if self._container.unigrams_probability >= self._container.bigrams_probability:
                    self._container.tonal = self._container.unigrams_tonal
                    self._container.probability = self._container.unigrams_probability

                else:
                    self._container.tonal = self._container.bigrams_tonal
                    self._container.probability = self._container.bigrams_probability

            elif self._container.unigrams_tonal == self._container.bigrams_tonal:
                    self._container.tonal = self._container.unigrams_tonal
                    self._container.probability = max(self._container.bigrams_probability,
                                                      self._container.unigrams_probability)

        elif self._container.unigrams_tonal:
            self._container.tonal = self._container.unigrams_tonal
            self._container.probability = self._container.unigrams_probability

        else:
            self._container.tonal = 'Unknown'

        self.__logger.info('Final tonal: %s' % self._container.tonal, 'Classifier.predict()')
        self.__logger.info('Final probability: %f' % self._container.probability, 'Classifier.predict()')

        return self._container.tonal, self._container.probability
