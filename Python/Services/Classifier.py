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

from threading import Thread
from sklearn.externals import joblib
from Python.Services.Logger import Logger
from Python.Services.PathService import PathService


class Classifier:
    def __init__(self):
        # Services
        self.__logger = Logger()

        if not self.__logger.configured:
            self.__logger.configure()

        self._path_service = PathService()

        # Data
        self._classifier_name = None
        self._unigrams_classifier = None
        self._bigrams_classifier = None
        self._trigrams_classifier = None

        self._unigrams_tonal = None
        self._bigrams_tonal = None
        self._trigrams_tonal = None

        self._unigrams_weight = None
        self._bigrams_weight = None
        self._trigrams_weight = None

        self._unigrams_probability = 0
        self._bigrams_probability = 0
        self._trigrams_probability = 0

        self.tonal = None
        self.probability = 0

        self.__logger.info('Classifier was successfully initialized.', 'Classifier.__init__()')

    def configure(self, classifier_name, unigrams_weight, bigrams_weight, trigrams_weight):
        self._classifier_name = classifier_name
        self._unigrams_weight = unigrams_weight
        self._bigrams_weight = bigrams_weight
        self._trigrams_weight = trigrams_weight

        self._unigrams_classifier = None
        self._bigrams_classifier = None
        self._trigrams_classifier = None

        self._unigrams_probability = 0
        self._bigrams_probability = 0
        self._trigrams_probability = 0

        self._unigrams_tonal = None
        self._bigrams_tonal = None
        self._trigrams_tonal = None

        try:
            if self._unigrams_weight:
                self._unigrams_classifier = joblib.load(self._path_service.get_path_to_model(self._classifier_name,
                                                                                             'unigrams'))

            if self._bigrams_weight:
                self._bigrams_classifier = joblib.load(self._path_service.get_path_to_model(self._classifier_name,
                                                                                            'bigrams'))

            if self._trigrams_weight:
                self._trigrams_classifier = joblib.load(self._path_service.get_path_to_model(self._classifier_name,
                                                                                             'trigrams'))

            self.__logger.info('Models were successfully loaded.', 'Classifier.configure()')
            self.__logger.info('Classifier was successfully configured.', 'Classifier.configure()')

        except FileNotFoundError or FileExistsError:
            self.__logger.fatal('File not found: %s' % str(FileNotFoundError.filename), 'Classifier.configure()')

    def _predict_unigrams(self):
        self._unigrams_tonal = self._unigrams_classifier.predict(self._unigrams_weight)[0]
        self._unigrams_probability = max(self._unigrams_classifier.predict_proba(self._unigrams_weight)[0])

        self.__logger.info('Unigrams tonal: %s' % self._unigrams_tonal, 'Classifier.predict()')
        self.__logger.info('Unigrams probability: %f' % self._unigrams_probability, 'Classifier.predict()')

    def _predict_bigrams(self):
        self._bigrams_tonal = self._bigrams_classifier.predict([[self._unigrams_weight, self._bigrams_weight]])[0]
        self._bigrams_probability = max(self._bigrams_classifier.predict_proba([[self._unigrams_weight,
                                                                                 self._bigrams_weight]])[0])

        self.__logger.info('Bigrams tonal: %s' % self._bigrams_tonal, 'Classifier.predict()')
        self.__logger.info('Bigrams probability: %f' % self._bigrams_probability, 'Classifier.predict()')

    def _predict_trigrams(self):
        self._trigrams_tonal = self._trigrams_classifier.predict([[self._unigrams_weight, self._bigrams_weight,
                                                                   self._trigrams_weight]])[0]
        self._trigrams_probability = max(self._trigrams_classifier.predict_proba([[self._unigrams_weight,
                                                                                   self._bigrams_weight,
                                                                                   self._trigrams_weight]])[0])

        self.__logger.info('Trigrams tonal: %s' % self._trigrams_tonal, 'Classifier.predict()')
        self.__logger.info('Trigrams probability: %f' % self._trigrams_probability, 'Classifier.predict()')

    def predict(self):
        if self._unigrams_weight:
            u_thread = Thread(target=self._predict_unigrams, args=())
            u_thread.start()
            u_thread.join()

            # self._unigrams_tonal = self._unigrams_classifier.predict(self._unigrams_weight)[0]
            # self._unigrams_probability = max(self._unigrams_classifier.predict_proba(self._unigrams_weight)[0])
            #
            # self.__logger.info('Unigrams tonal: %s' % self._unigrams_tonal, 'Classifier.predict()')
            # self.__logger.info('Unigrams probability: %f' % self._unigrams_probability, 'Classifier.predict()')

        if self._bigrams_weight:
            b_thread = Thread(target=self._predict_bigrams, args=())
            b_thread.start()
            b_thread.join()

            # self._bigrams_tonal = self._bigrams_classifier.predict([[self._unigrams_weight, self._bigrams_weight]])[0]
            # self._bigrams_probability = max(self._bigrams_classifier.predict_proba([[self._unigrams_weight,
            #                                                                          self._bigrams_weight]])[0])
            #
            # self.__logger.info('Bigrams tonal: %s' % self._bigrams_tonal, 'Classifier.predict()')
            # self.__logger.info('Bigrams probability: %f' % self._bigrams_probability, 'Classifier.predict()')

        if self._trigrams_weight:
            t_thread = Thread(target=self._predict_trigrams, args=())
            t_thread.start()
            t_thread.join()

            # self._trigrams_tonal = self._trigrams_classifier.predict([[self._unigrams_weight, self._bigrams_weight,
            #                                                            self._trigrams_weight]])[0]
            # self._trigrams_probability = max(self._trigrams_classifier.predict_proba([[self._unigrams_weight,
            #                                                                            self._bigrams_weight,
            #                                                                            self._trigrams_weight]])[0])
            #
            # self.__logger.info('Trigrams tonal: %s' % self._trigrams_tonal, 'Classifier.predict()')
            # self.__logger.info('Trigrams probability: %f' % self._trigrams_probability, 'Classifier.predict()')

        if self._unigrams_tonal and self._bigrams_tonal and self._trigrams_tonal:

            if self._unigrams_tonal == self._bigrams_tonal:
                self.tonal = self._unigrams_tonal
                self.probability = max(self._unigrams_probability, self._bigrams_probability)

            elif self._unigrams_tonal == self._trigrams_tonal:
                self.tonal = self._unigrams_tonal
                self.probability = max(self._unigrams_probability, self._trigrams_probability)

            elif self._bigrams_tonal == self._trigrams_tonal:
                self.tonal = self._bigrams_tonal
                self.probability = max(self._bigrams_probability, self._trigrams_probability)

        elif self._unigrams_tonal and self._bigrams_tonal:

            if self._unigrams_tonal != self._bigrams_tonal:
                if self._unigrams_probability >= self._bigrams_probability:
                    self.tonal = self._unigrams_tonal
                    self.probability = self._unigrams_probability

                else:
                    self.tonal = self._bigrams_tonal
                    self.probability = self._bigrams_probability

            elif self._unigrams_tonal == self._bigrams_tonal:
                    self.tonal = self._unigrams_tonal
                    self.probability = max(self._bigrams_probability, self._unigrams_probability)

        elif self._unigrams_tonal:
            self.tonal = self._unigrams_tonal
            self.probability = self._unigrams_probability

        else:
            self.tonal = 'Unknown'

        self.__logger.info('Final tonal: %s' % self.tonal, 'Classifier.predict()')
        self.__logger.info('Final probability: %f' % self.probability, 'Classifier.predict()')

        return self.tonal, self.probability
