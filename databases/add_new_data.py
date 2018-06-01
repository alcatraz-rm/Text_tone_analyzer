import sqlite3
import csv
import os
import progressbar
from modules.lemmatization.lemmatization import lemmatization
from modules.get_ngram_info.get_ngram_info import get_ngram_info
from modules.count_text_tonal.count_text_tonal import Document
from datetime import datetime
import logging
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
import pandas
import platform

system = platform.system().lower()
cwd = os.getcwd()
time = str(datetime.now()).replace(':', '-')
logging.basicConfig(filename=os.path.join('logs', 'log_%s.log' % time), filemode='w', level=logging.INFO)
logging.info('\nadd_new_data\n')
logging.info('\noperation system: %s\n' % system)
logging.info('\nCWD: %s' % cwd)

# create copies of datasets
with open('dataset_with_unigrams.csv', 'r', encoding='utf-8') as src:
    with open('dataset_with_unigrams_copy.csv', 'w', encoding='utf-8') as cp:
        cp.write(src.read())

with open('dataset_with_bigrams.csv', 'r', encoding='utf-8') as src:
    with open('dataset_with_bigrams_copy.csv', 'w', encoding='utf-8') as cp:
        cp.write(src.read())

with open('dataset_with_trigrams.csv', 'r', encoding='utf-8') as src:
    with open('dataset_with_trigrams_copy.csv', 'w', encoding='utf-8') as cp:
        cp.write(src.read())

logging.info('\ncopies of datasets was successfully created\n')

changes_date = str(datetime.now())

u = sqlite3.connect('unigrams.db')
u_cursor = u.cursor()

b = sqlite3.connect('bigrams.db')
b_cursor = b.cursor()

t = sqlite3.connect('trigrams.db')
t_cursor = t.cursor()

logging.info('\ndatabases was successfully connected\n')


def read_data():
    with open(os.path.join('..', 'tests', 'data_to_add.csv'), 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list()
        for row in reader:
            doc = ''.join(row).split(';')
            data.append({'text': doc[0], 'tonal': doc[1]})

        logging.info('\nnew documents was successfully read\n')
        return data


def lemmatization_all_data(data):
    print('lemmatization...')
    with progressbar.ProgressBar(max_value=len(data)) as bar:
        for n in range(len(data)):
            data[n]['text'] = lemmatization(data[n]['text'])
            bar.update(n)

    logging.info('\nlemmatization of new data was successfully finished\n')
    return data


def split_into_bigrams(text):
    unigrams = text.split()
    return [unigrams[n] + ' ' + unigrams[n + 1] for n in range(len(text.split()) - 1)]


def split_into_trigrams(text):
    unigrams = text.split()
    return [unigrams[n] + ' ' + unigrams[n + 1] + ' ' + unigrams[n + 2] for n in range(len(text.split()) - 2)]


def split_into_ngrams(data):
    print('\nsplitting documents into N-grams...')
    unigrams = list()
    bigrams = list()
    trigrams = list()

    with progressbar.ProgressBar(max_value=len(data)) as bar:
        for n, doc in enumerate(data):
            for unigram in doc['text'].split():
                if unigram not in unigrams:
                    unigrams.append(unigram)

            for bigram in split_into_bigrams(doc['text']):
                if bigram not in bigrams:
                    bigrams.append(bigram)

            for trigram in split_into_trigrams(doc['text']):
                if trigram not in trigrams:
                    trigrams.append(trigram)
            bar.update(n)

    logging.info('\nnew documents was successfully splited into N-grams\n')
    return unigrams, bigrams, trigrams


def check_ngram(ngram):
    data = get_ngram_info(ngram)
    if data and data[0]:
        return True
    else:
        return False


def count_occurrences(ngram, data):
    pos_count = 1
    neg_count = 1

    for doc in data:
        if ngram in doc['text']:
            if doc['tonal'] == 'positive':
                pos_count += 1
            else:
                neg_count += 1

    return pos_count, neg_count


def read_dataset(mode):
    data = list()
    if mode == 'unigrams':
        filename = 'dataset_with_unigrams.csv'
    elif mode == 'bigrams':
        filename = 'dataset_with_bigrams.csv'
    elif mode == 'trigrams':
        filename = 'dataset_with_trigrams.csv'
    else:
        return None

    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(''.join(row).split(';'))

    logging.info('\ndataset was successfully read, mode: %s\n' % mode)
    return data


def delta_tf_idf_count(text):
    doc = Document(text)
    doc.count_weight_by_unigrams()
    doc.count_weight_by_bigrams()
    doc.count_weight_by_trigrams()

    return doc.unigrams_weight, doc.bigrams_weight, doc.trigrams_weight


def count_all_occurrences(unigrams, bigrams, trigrams, data):
    unigrams_new = dict()
    bigrams_new = dict()
    trigrams_new = dict()

    for unigram in unigrams:
        unigram_occurrences = count_occurrences(unigram, data)
        if unigram_occurrences:
            unigrams_new[unigram] = unigram_occurrences

    for bigram in bigrams:
        bigram_occurrences = count_occurrences(bigram, data)
        if bigram_occurrences:
            bigrams_new[bigram] = bigram_occurrences

    for trigram in trigrams:
        trigram_occurrences = count_occurrences(trigram, data)
        if trigram_occurrences:
            trigrams_new[trigram] = trigram_occurrences

    logging.info('\nall occurrences of N-grams was counted\n')
    return unigrams_new, bigrams_new, trigrams_new


def update_value(ngram, pos_count, neg_count):
    data = get_ngram_info(ngram)
    pos_count += data[0]
    neg_count += data[1]

    if ngram.count(' ') == 0:
        u_cursor.execute("""UPDATE Data
                            SET Pos_count = %d
                            WHERE Ngram = '%s'""" % (pos_count, ngram))
        u_cursor.execute("""UPDATE Data
                            SET Neg_count = %d
                            WHERE Ngram = '%s'""" % (neg_count, ngram))
        u_cursor.execute("""UPDATE Data
                            SET Changes_Date = '%s'
                            WHERE Ngram = '%s'""" % (changes_date, ngram))
        u.commit()

    elif ngram.count(' ') == 1:
        b_cursor.execute("""UPDATE Data
                            SET Pos_count = %d
                            WHERE Ngram = '%s'""" % (pos_count, ngram))
        b_cursor.execute("""UPDATE Data
                            SET Neg_count = %d
                            WHERE Ngram = '%s'""" % (neg_count, ngram))
        b_cursor.execute("""UPDATE Data
                            SET Changes_Date = '%s'
                            WHERE Ngram = '%s'""" % (changes_date, ngram))
        b.commit()

    elif ngram.count(' ') == 2:
        t_cursor.execute("""UPDATE Data
                            SET Pos_count = %d
                            WHERE Ngram = '%s'""" % (pos_count, ngram))
        t_cursor.execute("""UPDATE Data
                            SET Neg_count = %d
                            WHERE Ngram = '%s'""" % (neg_count, ngram))
        t_cursor.execute("""UPDATE Data
                            SET Changes_Date = '%s'
                            WHERE Ngram = '%s'""" % (changes_date, ngram))
        t.commit()


def add_value(ngram, pos_count, neg_count):
    if ngram.count(' ') == 0:
        u_cursor.execute("""INSERT INTO 'Data'
                            VALUES ('%s', %d, %d, %d, '%s')""" % (ngram, pos_count, neg_count, 1, changes_date))
        u.commit()

    elif ngram.count(' ') == 1:
        b_cursor.execute("""INSERT INTO 'Data'
                            VALUES ('%s', %d, %d, %d, '%s')""" % (ngram, pos_count, neg_count, 1, changes_date))
        b.commit()

    elif ngram.count(' ') == 2:
        t_cursor.execute("""INSERT INTO 'Data'
                            VALUES ('%s', %d, %d, %d, '%s')""" % (ngram, pos_count, neg_count, 1, changes_date))
        t.commit()


def update_db(unigrams, bigrams, trigrams):
    with progressbar.ProgressBar(max_value=len(unigrams) + len(bigrams) + len(trigrams)) as bar:
        k = 0
        for unigram, occurrences in unigrams.items():
            if check_ngram(unigram):
                update_value(unigram, *occurrences)
            else:
                add_value(unigram, *occurrences)
            k += 1
            bar.update(k)

        logging.info('\nunigrams database was successfully updated\n')

        for bigram, occurrences in bigrams.items():
            if check_ngram(bigram):
                update_value(bigram, *occurrences)
            else:
                add_value(bigram, *occurrences)
            k += 1
            bar.update(k)

        logging.info('\nbigrams database was successfully updated\n')

        for trigram, occurrences in trigrams.items():
            if check_ngram(trigram):
                update_value(trigram, *occurrences)
            else:
                add_value(trigram, *occurrences)
            k += 1
            bar.update(k)

        logging.info('\ntrigrams database was successfully updated\n')


def update_datasets(data):
    with open('dataset_with_unigrams.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        texts = [[''.join(row).split(';')[0], ''.join(row).split(';')[1]] for row in reader]  # read all documents

    # append new documents
    for doc in data:
        if [doc['text'], doc['tonal']] not in texts:
            texts.append([doc['text'], doc['tonal']])

    with open('dataset_with_unigrams.csv', 'w', encoding='utf-8') as unigrams:
        with open('dataset_with_bigrams.csv', 'w', encoding='utf-8') as bigrams:
            with open('dataset_with_trigrams.csv', 'w', encoding='utf-8') as trigrams:
                for text in texts:
                    unigrams_weight, bigrams_weight, trigrams_weight = delta_tf_idf_count(text[0])

                    if trigrams_weight:
                        trigrams.write(text[0] + ';' + text[1] + ';' + unigrams_weight + ';' + bigrams_weight +
                                       ';' + trigrams_weight + '\n')
                        bigrams.write(text[0] + ';' + text[1] + ';' + unigrams_weight + ';' + bigrams_weight +
                                      '\n')
                        unigrams.write(text[0] + ';' + text[1] + ';' + unigrams_weight + '\n')

                    elif bigrams_weight:
                        bigrams.write(text[0] + ';' + text[1] + ';' + unigrams_weight + ';' + bigrams_weight +
                                      '\n')
                        unigrams.write(text[0] + ';' + text[1] + ';' + unigrams_weight + '\n')

                    else:
                        unigrams.write(text[0] + ';' + text[1] + ';' + unigrams_weight + '\n')

    logging.info('\ndatasets was successfully updated\n')


def read_training_data(dataset):
    training_data = dict()
    data = pandas.read_csv('dataset_with_%s.csv' % dataset, sep=';', encoding='utf-8')

    training_data['features'] = data.loc()[:, ['unigrams_weight', 'bigrams_weight']]
    training_data['labels'] = data['tonal']

    return training_data


def model_fit(classifier_name, training_data, dataset):
    classifier = None
    if classifier_name == 'nbc':
        classifier = GaussianNB()
    elif classifier_name == 'logreg':
        classifier = LogisticRegression()
    elif classifier_name == 'knn':
        classifier = KNeighborsClassifier(250)
    elif classifier_name == 'decision_tree':
        classifier = DecisionTreeClassifier()

    classifier.fit(training_data['features'], training_data['labels'])
    joblib.dump(classifier, os.path.join('models', classifier_name, 'model_%s.pkl' % dataset), compress=9)


def fit_the_models():
    classifiers_names = ['nbc', 'logreg', 'knn', 'desicion_tree']
    datasets_names = ['unigrams', 'bigrams', 'trigrams']

    with progressbar.ProgressBar(max_value=len(classifiers_names) * len(datasets_names)) as bar:
        k = 0
        for classifiers_name in classifiers_names:
            for dataset_name in datasets_names:
                training_data = read_training_data(dataset_name)
                model_fit(classifiers_name, training_data, dataset_name)
                k += 1
                bar.update(k)
                logging.info('\nmodel was successfully fitted, params: (%s, %s)\n' % (classifiers_name, dataset_name))


def delete_files():
    os.remove('dataset_with_unigrams_copy.csv')
    os.remove('dataset_with_bigrams_copy.csv')
    os.remove('dataset_with_trigrams_copy.csv')

    with open(os.path.join('..', 'tests', 'data_to_add.csv'), 'w', encoding='utf-8'):
        pass


data = lemmatization_all_data(read_data())
unigrams, bigrams, trigrams = count_all_occurrences(*split_into_ngrams(data), data)
update_db(unigrams, bigrams, trigrams)
update_datasets(data)
fit_the_models()
delete_files()
