# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


import sqlite3
import csv
import os
import progressbar
from modules.lemmatization.lemmatization import lemmatization
from modules.get_ngram_info.get_ngram_info import get_ngram_info
from modules.count_text_tonal.count_text_tonal import Document
from datetime import datetime
import copy
import pandas
from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib
import logging
import platform

if not os.path.exists('logs'):
    os.mkdir('logs')

system = platform.system().lower()
cwd = os.getcwd()

time = str(datetime.now()).replace(':', '-')
logging.basicConfig(filename=os.path.join('logs', 'log_%s.log' % time), filemode='w', level=logging.INFO)
logging.info('\nadd_new_data.py\n')
logging.info('\noperation system: %s\n' % system)
logging.info('\nCWD: %s' % cwd)

# create copies of datasets
with open('dataset_with_unigrams.csv', 'r', encoding='utf-8') as src:
    with open('dataset_with_unigrams_copy.csv', 'w', encoding='utf-8') as cp:
        cp.write(src.read())
logging.info('\nunigrams dataset was successfully copied\n')

with open('dataset_with_bigrams.csv', 'r', encoding='utf-8') as src:
    with open('dataset_with_bigrams_copy.csv', 'w', encoding='utf-8') as cp:
        cp.write(src.read())
logging.info('\nbigrams dataset was successfully copied\n')

with open('dataset_with_trigrams.csv', 'r', encoding='utf-8') as src:
    with open('dataset_with_trigrams_copy.csv', 'w', encoding='utf-8') as cp:
        cp.write(src.read())
logging.info('\ntrigrams dataset was successfully copied\n')

changes_date = str(datetime.now())

u = sqlite3.connect('unigrams.db')
u_cursor = u.cursor()
logging.info('\nunigrams DB was successfully connected\n')

b = sqlite3.connect('bigrams.db')
b_cursor = b.cursor()
logging.info('\nbigrams DB was successfully connected\n')

t = sqlite3.connect('trigrams.db')
t_cursor = t.cursor()
logging.info('\ntrigrams DB was successfully connected\n')


def read_data():
    logging.info('\nread_data\n')
    with open(os.path.join('..', 'tests', 'data_to_add.csv'), 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list()
        for row in reader:
            doc = ''.join(row).split(';')
            data.append({'text': doc[0], 'tonal': doc[1]})

    logging.info('\ndata to add was successfully readedn\n')

    return data


def lemmatization_all_data(data):
    print('lemmatization...')
    logging.info('\nlemmatization\n')
    with progressbar.ProgressBar(max_value=len(data)) as bar:
        for n in range(len(data)):
            data[n]['text'] = lemmatization(data[n]['text'])
            bar.update(n)

    logging.info('\nlemmatization was successfully finished\n')

    return data


def split_into_bigrams(text):
    unigrams = text.split()
    return [unigrams[n] + ' ' + unigrams[n + 1] for n in range(len(text.split()) - 1)]


def split_into_trigrams(text):
    unigrams = text.split()
    return [unigrams[n] + ' ' + unigrams[n + 1] + ' ' + unigrams[n + 2] for n in range(len(text.split()) - 2)]


def split_into_ngrams(data):
    print('\nsplitting documents into N-grams...')
    logging.info('\nsplit_documents_into_ngrams\n')
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

    logging.info('\ndocuments was successfully splitted into N-grams\n')
    return unigrams, bigrams, trigrams


def check_ngram(ngram):
    data = get_ngram_info(ngram)
    if data and data[0]:
        return True
    else:
        return False


def split_ngrams_by_status(unigrams, bigrams, trigrams):
    print('\nsplitting N-grams by database status...')
    logging.info('\nsplit ngrams by database status\n')

    new_unigrams = {'true': list(), 'false': list()}
    new_bigrams = {'true': list(), 'false': list()}
    new_trigrams = {'true': list(), 'false': list()}

    with progressbar.ProgressBar(max_value=len(unigrams) + len(bigrams) + len(trigrams)) as bar:
        k = 0
        for unigram in unigrams:
            if check_ngram(unigram):
                new_unigrams['true'].append(unigram)
            else:
                new_unigrams['false'].append(unigram)
            k += 1
            bar.update(k)

        for bigram in bigrams:
            if check_ngram(bigram):
                new_bigrams['true'].append(bigram)
            else:
                new_bigrams['false'].append(bigram)
            k += 1
            bar.update(k)

        for trigram in trigrams:
            if check_ngram(trigram):
                new_trigrams['true'].append(trigram)
            else:
                new_trigrams['false'].append(trigram)
            k += 1
            bar.update(k)

    logging.info('\ndocuments was successfully splitted by database status\n')
    return new_unigrams, new_bigrams, new_trigrams


def update_value(ngram, pos_count, neg_count):
    data = get_ngram_info(ngram)
    pos_count += data[1]
    neg_count += data[2]

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


def add_ngrams_to_db(unigrams, bigrams, trigrams, data):
    logging.info('\nadd_ngrams_to_dbn\n')
    print('\nadding true values...')
    logging.info('\nadd true values\n')

    with progressbar.ProgressBar(max_value=(len(unigrams['true']) + len(bigrams['true']) + len(trigrams['true']))) as bar:
        k = 0
        for unigram in unigrams['true']:
            update_value(unigram, *count_occurrences(unigram, data))
            k += 1
            bar.update(k)

        for bigram in bigrams['true']:
            update_value(bigram, *count_occurrences(bigram, data))
            k += 1
            bar.update(k)

        for trigram in trigrams['true']:
            update_value(trigram, *count_occurrences(trigram, data))
            k += 1
            bar.update(k)

    logging.info('\ntrue values was successfully added\n')

    print('\nadding false values...')
    logging.info('\nadd false values\n')

    with progressbar.ProgressBar(max_value=len(unigrams['false']) + len(bigrams['false']) + len(trigrams['false'])) as bar:
        k = 0
        for unigram in unigrams['false']:
            add_value(unigram, *count_occurrences(unigram, data))
            k += 1
            bar.update(k)

        for bigram in bigrams['false']:
            add_value(bigram, *count_occurrences(bigram, data))
            k += 1
            bar.update(k)

        for trigram in trigrams['false']:
            add_value(trigram, *count_occurrences(trigram, data))
            k += 1
            bar.update(k)

    logging.info('\nfalse values was successfully added\n')


def read_dataset(mode):
    logging.info('\nread dataset\n')
    logging.info('mode: %s' % mode)

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

    logging.info('dataset_was_successfully readed\n')
    return data


def delta_tf_idf_count(text):
    doc = Document(text)
    doc.count_weight_by_unigrams()
    doc.count_weight_by_bigrams()
    doc.count_weight_by_trigrams()

    return doc.unigrams_weight, doc.bigrams_weight, doc.trigrams_weight


def read_training_data(mode):
    logging.info('\nread training data\n')
    logging.info('mode: %s' % mode)

    training_data = dict()
    data = pandas.read_csv(os.path.join('..', 'databases', 'dataset_with_%s.csv' % mode), sep=';', encoding='utf-8')

    if mode == 'unigrams':
        training_data['features'] = data.loc()[:, ['unigrams_weight']]
    elif mode == 'bigrams':
        training_data['features'] = data.loc()[:, ['unigrams_weight', 'bigrams_weight']]
    elif mode == 'trigrams':
        training_data['features'] = data.loc()[:, ['unigrams_weight', 'bigrams_weight', 'trigrams_weight']]

    training_data['labels'] = data['tonal']

    logging.info('\ntraining data was successfully readed\n')

    return training_data


def model_fit(mode, training_data):
    logging.info('\nmodel fit\n')
    logging.info('mode: %s\n' % mode)

    classifier = GaussianNB()
    classifier.fit(training_data['features'], training_data['labels'])
    joblib.dump(classifier, os.path.join('models', 'nbc', 'model_%s.pkl' % mode), compress=9)

    logging.info('model was successfully fitted')


def rewrite_datasets(data):
    logging.info('\nrewrite_datasets\n')

    texts = list()
    unigrams_dataset = read_dataset('unigrams')
    bigrams_dataset = read_dataset('bigrams')
    trigrams_dataset = read_dataset('trigrams')

    logging.info('\ncreate full dataset\n')
    for doc in trigrams_dataset:
        texts.append([doc[0], doc[1]])

    logging.info('docs from trigrams dataset was successfully added\n')

    for doc in bigrams_dataset:
        if doc[0] not in texts:
            texts.append([doc[0], doc[1]])

    logging.info('docs from bigrams dataset was successfully added\n')

    for doc in unigrams_dataset:
        if doc[0] not in texts:
            texts.append([doc[0], doc[1]])

    logging.info('docs from unigrams dataset was successfully added\n')

    for text in data:
        if [text['text'], text['tonal']] not in texts:
            texts.append([text['text'], text['tonal']])

    logging.info('new docs was successfully added\n')

    logging.info('\nadd docs to datasets\n')

    with progressbar.ProgressBar(max_value=len(texts)) as bar:
        for n, doc in enumerate(texts):
            unigrams_weight, bigrams_weight, trigrams_weight = delta_tf_idf_count(doc[0])
            if trigrams_weight:
                texts[n].append(unigrams_weight)
                texts[n].append(bigrams_weight)
                texts[n].append(trigrams_weight)
            elif bigrams_weight:
                texts[n].append(unigrams_weight)
                texts[n].append(bigrams_weight)
            elif unigrams_weight:
                texts[n].append(unigrams_weight)

            bar.update(n)

            texts = copy.deepcopy(texts)

    with open('dataset_with_unigrams.csv', 'w', encoding='utf-8') as u:
        with open('dataset_with_bigrams.csv', 'w', encoding='utf-8') as b:
            with open('dataset_with_trigrams.csv', 'w', encoding='utf-8') as t:
                for doc in texts:
                    if len(doc) == 5:
                        u.write(';'.join(doc) + '\n')
                        b.write(';'.join(doc) + '\n')
                        t.write(';'.join(doc) + '\n')
                    elif len(doc) == 4:
                        u.write(';'.join(doc) + '\n')
                        b.write(';'.join(doc) + '\n')
                    elif len(doc) == 3:
                        u.write(';'.join(doc) + '\n')

    logging.info('docs was successfully added to datasets\n')


def models_fit():
    logging.info('\nmodels fit\n')

    logging.info('\nread training data\n')

    unigrams_dataset = read_training_data('unigrams')
    bigrams_dataset = read_training_data('bigrams')
    trigrams_dataset = read_training_data('trigrams')

    logging.info('trainig data was successfully readed\n')

    logging.info('\nfit models\n')

    model_fit('unigrams', unigrams_dataset)
    model_fit('bigrams', bigrams_dataset)
    model_fit('trigrams', trigrams_dataset)

    logging.info('models was successfully fitted\n')


data = lemmatization_all_data(read_data())
unigrams, bigrams, trigrams = split_ngrams_by_status(*split_into_ngrams(data))
add_ngrams_to_db(unigrams, bigrams, trigrams, data)
rewrite_datasets(data)

os.remove('dataset_with_unigrams_copy.csv')
os.remove('dataset_with_bigrams_copy.csv')
os.remove('dataset_with_trigrams_copy.csv')
