from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer


def read_data():
    positive = list()
    negative = list()

    with open('dataset_labels.csv', 'r', encoding='utf-8') as file:
        for document in file.readlines():
            data = document.split(';')

            if data[1] == 'positive':
                positive.append(data[0])
            else:
                negative.append(data[0])

    return positive, negative


def fit_vectorizer(dataset):
    vectorizer = TfidfVectorizer()
    vectorizer.fit(dataset)

    return vectorizer


def dump_vectorizer(name, vectorizer):
    joblib.dump(vectorizer, name, compress=9)


positive, negative = read_data()

positive_vectorizer = fit_vectorizer(positive)
negative_vectorizer = fit_vectorizer(negative)

dump_vectorizer('positive_vectorizer.pkl', positive_vectorizer)
dump_vectorizer('negative_vectorizer.pkl', negative_vectorizer)
