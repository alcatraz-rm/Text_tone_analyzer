import os

import pandas
from sklearn.externals import joblib
from sklearn.naive_bayes import GaussianNB

cwd = os.getcwd()


def read_training_data():
    training_data = dict()
    data = pandas.read_csv(os.path.join('..', '..', 'Databases', 'dataset_with_trigrams.csv'), sep=';',
                           encoding='utf-8')

    training_data['features'] = data.loc()[:, ['unigrams_weight', 'bigrams_weight', 'trigrams_weight']]
    training_data['labels'] = data['tonal']

    return training_data


def model_fit(classifier, training_data):
    classifier.fit(training_data['features'], training_data['labels'])
    joblib.dump(classifier, 'model_trigrams.pkl', compress=9)


training_data = read_training_data()
classifier = GaussianNB()
model_fit(classifier, training_data)
