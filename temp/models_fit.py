from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
import os
import pandas
cwd = os.getcwd()


def read_training_data():
    training_data = dict()
    data = pandas.read_csv(os.path.join('..', 'databases', 'dataset_with_trigrams.csv'), sep=';', encoding='utf-8')

    training_data['features'] = data.loc()[:, ['unigrams_weight', 'bigrams_weight', 'trigrams_weight']]
    training_data['labels'] = data['tonal']

    return training_data


def model_fit(classifier, training_data):
    classifier.fit(training_data['features'], training_data['labels'])
    joblib.dump(classifier, 'model_trigrams.pkl', compress=9)


training_data = read_training_data()
classifier = DecisionTreeClassifier()
model_fit(classifier, training_data)
