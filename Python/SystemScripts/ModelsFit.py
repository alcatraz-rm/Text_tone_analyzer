import os

import pandas
from sklearn.externals import joblib
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

cwd = os.getcwd()


def read_training_data(mode):
    training_data = dict()
    data = pandas.read_csv(os.path.join('..', '..', 'Data', 'dataset_with_trigrams.csv'), sep=';',
                           encoding='utf-8')

    if mode == 'unigrams':
        training_data['features'] = data.loc()[:, ['unigrams_weight']]
    elif mode == 'bigrams':
        training_data['features'] = data.loc()[:, ['unigrams_weight', 'bigrams_weight']]
    elif mode == 'trigrams':
        training_data['features'] = data.loc()[:, ['unigrams_weight', 'bigrams_weight', 'trigrams_weight']]

    training_data['labels'] = data['tonal']

    return training_data


def model_fit(classifier, mode):
    if mode == 'all':
        training_data = read_training_data('unigrams')
        classifier.fit(training_data['features'], training_data['labels'])
        joblib.dump(classifier, 'model_unigrams.pkl', compress=9)

        training_data = read_training_data('bigrams')
        classifier.fit(training_data['features'], training_data['labels'])
        joblib.dump(classifier, 'model_bigrams.pkl', compress=9)

        training_data = read_training_data('trigrams')
        classifier.fit(training_data['features'], training_data['labels'])
        joblib.dump(classifier, 'model_trigrams.pkl', compress=9)


def read_info():
    classifier_to_fit = input('classifier to fit: ').strip()
    mode = input('mode (all, unigrams, bigrams, trigrams): ').lower().strip()

    if classifier_to_fit == 'NBC':
        print('NBC')
        classifier = GaussianNB()

    elif classifier_to_fit == 'LogisticRegression':
        print('LogisticRegression')
        classifier = LogisticRegression()

    elif classifier_to_fit == 'KNN':
        print('KNN')
        classifier = KNeighborsClassifier(250)

    elif classifier_to_fit == 'RandomForest':
        print('RandomForest')
        classifier = RandomForestClassifier(n_estimators=150)

    else:
        print('NBC')
        classifier = GaussianNB()

    if mode not in ['all', 'unigrams', 'bigrams', 'trigrams']:
        mode = 'all'

    return classifier, mode


classifier, mode = read_info()
model_fit(classifier, mode)
