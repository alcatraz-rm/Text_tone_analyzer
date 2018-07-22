# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import os
from sklearn.externals import joblib
from Python.Services.Logger import Logger


class Classifier:
    def __init__(self):
        # Services
        self.__logger = Logger()

        if not self.__logger.configured:
            self.__logger.configure()

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

        path_to_models = None

        if os.getcwd().endswith('Python'):
            path_to_models = os.path.join('..', 'Databases', 'Models')

        elif os.getcwd().endswith('Tests'):
            path_to_models = os.path.join('..', '..', 'Databases', 'Models')

        try:
            if self._unigrams_weight:
                self._unigrams_classifier = joblib.load(os.path.join(path_to_models,
                                                                     self._classifier_name, 'model_unigrams.pkl'))

            if self._bigrams_weight:
                self._bigrams_classifier = joblib.load(os.path.join(path_to_models,
                                                                    self._classifier_name, 'model_bigrams.pkl'))

            if self._trigrams_weight:
                self._trigrams_classifier = joblib.load(os.path.join(path_to_models,
                                                                     self._classifier_name, 'model_trigrams.pkl'))

            self.__logger.info('Models were successfully loaded.', 'Classifier.configure()')
            self.__logger.info('Classifier was successfully configured.', 'Classifier.configure()')

        except FileNotFoundError or FileExistsError:
            self.__logger.fatal('File not found: %s' % FileNotFoundError.filename, 'Classifier.configure()')

    def predict(self):
        if self._unigrams_weight:
            self._unigrams_tonal = self._unigrams_classifier.predict(self._unigrams_weight)[0]
            self._unigrams_probability = max(self._unigrams_classifier.predict_proba(self._unigrams_weight)[0])

            self.__logger.info('Unigrams tonal: %s' % self._unigrams_tonal, 'Classifier.predict()')
            self.__logger.info('Unigrams probability: %f' % self._unigrams_probability, 'Classifier.predict()')

        if self._bigrams_weight:
            self._bigrams_tonal = self._bigrams_classifier.predict([[self._unigrams_weight, self._bigrams_weight]])[0]
            self._bigrams_probability = max(self._bigrams_classifier.predict_proba([[self._unigrams_weight,
                                                                                     self._bigrams_weight]])[0])

            self.__logger.info('Bigrams tonal: %s' % self._bigrams_tonal, 'Classifier.predict()')
            self.__logger.info('Bigrams probability: %f' % self._bigrams_probability, 'Classifier.predict()')

        if self._trigrams_weight:
            self._trigrams_tonal = self._trigrams_classifier.predict([[self._unigrams_weight, self._bigrams_weight,
                                                                       self._trigrams_weight]])[0]
            self._trigrams_probability = max(self._trigrams_classifier.predict_proba([[self._unigrams_weight,
                                                                                       self._bigrams_weight, self._trigrams_weight]])[0])

            self.__logger.info('Trigrams tonal: %s' % self._trigrams_tonal, 'Classifier.predict()')
            self.__logger.info('Trigrams probability: %f' % self._trigrams_probability, 'Classifier.predict()')

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

        elif self._unigrams_tonal and self._bigrams_tonal and self._unigrams_tonal != self._bigrams_tonal:

            if self._unigrams_probability >= self._bigrams_probability:
                self.tonal = self._unigrams_tonal
                self.probability = self._unigrams_probability

            else:
                self.tonal = self._bigrams_tonal
                self.probability = self._bigrams_probability

        elif self._unigrams_tonal:
            self.tonal = self._unigrams_tonal
            self.probability = self._unigrams_probability

        else:
            self.tonal = 'Unknown'

        self.__logger.info('Final tonal: %s' % self.tonal, 'Classifier.predict()')
        self.__logger.info('Final probability: %f' % self.probability, 'Classifier.predict()')

        return self.tonal, self.probability
