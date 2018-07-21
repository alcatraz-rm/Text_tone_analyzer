# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

from sklearn.externals import joblib
from os import path


class Classifier:
    def __init__(self):
        self.classifier_name = None
        self.unigrams_classifier = None
        self.bigrams_classifier = None
        self.trigrams_classifier = None

        self.unigrams_tonal = None
        self.bigrams_tonal = None
        self.trigrams_tonal = None

        self.unigrams_weight = None
        self.bigrams_weight = None
        self.trigrams_weight = None

        self.unigrams_probability = 0
        self.bigrams_probability = 0
        self.trigrams_probability = 0

        self.tonal = None
        self.probability = 0

    def configure(self, classifier_name, unigrams_weight, bigrams_weight, trigrams_weight):
        self.classifier_name = classifier_name
        self.unigrams_weight = unigrams_weight
        self.bigrams_weight = bigrams_weight
        self.trigrams_weight = trigrams_weight

        self.unigrams_classifier = None
        self.bigrams_classifier = None
        self.trigrams_classifier = None

        self.unigrams_probability = 0
        self.bigrams_probability = 0
        self.trigrams_probability = 0

        self.unigrams_tonal = None
        self.bigrams_tonal = None
        self.trigrams_tonal = None

        try:
            if self.unigrams_weight:
                self.unigrams_classifier = joblib.load(path.join('..', '..', 'Databases', 'Models',
                                                                 self.classifier_name, 'model_unigrams.pkl'))

            if self.bigrams_weight:
                self.bigrams_classifier = joblib.load(path.join('..', '..', 'Databases', 'Models',
                                                                self.classifier_name, 'model_bigrams.pkl'))

            if self.trigrams_weight:
                self.trigrams_classifier = joblib.load(path.join('..', '..', 'Databases', 'Models',
                                                                 self.classifier_name, 'model_trigrams.pkl'))

        except FileNotFoundError or FileExistsError:
            pass

    def predict(self):
        if self.unigrams_weight:
            self.unigrams_tonal = self.unigrams_classifier.predict(self.unigrams_weight)[0]
            self.unigrams_probability = max(self.unigrams_classifier.predict_proba(self.unigrams_weight)[0])

        if self.bigrams_weight:
            self.bigrams_tonal = self.bigrams_classifier.predict([[self.unigrams_weight, self.bigrams_weight]])[0]
            self.bigrams_probability = max(self.bigrams_classifier.predict_proba([[self.unigrams_weight,
                                                                                   self.bigrams_weight]])[0])

        if self.trigrams_weight:
            self.trigrams_tonal = self.trigrams_classifier.predict([[self.unigrams_weight, self.bigrams_weight,
                                                                     self.trigrams_weight]])[0]
            self.trigrams_probability = max(self.trigrams_classifier.predict_proba([[self.unigrams_weight,
                                                                                     self.bigrams_weight, self.trigrams_weight]])[0])

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

        elif self.unigrams_tonal and self.bigrams_tonal and self.unigrams_tonal != self.bigrams_tonal:

            if self.unigrams_probability >= self.bigrams_probability:
                self.tonal = self.unigrams_tonal
                self.probability = self.unigrams_probability

            else:
                self.tonal = self.bigrams_tonal
                self.probability = self.bigrams_probability

        elif self.unigrams_tonal:
            self.tonal = self.unigrams_tonal
            self.probability = self.unigrams_probability

        else:
            self.tonal = 'Unknown'

        return self.tonal, self.probability
