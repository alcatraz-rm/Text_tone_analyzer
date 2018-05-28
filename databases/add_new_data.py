import sqlite3
import csv
import os
import progressbar
from modules.lemmatization.lemmatization import lemmatization
from modules.get_ngram_info.get_ngram_info import get_ngram_info
from modules.count_text_tonal.count_text_tonal import Document
from datetime import datetime
import copy

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

changes_date = str(datetime.now())

u = sqlite3.connect('unigrams.db')
u_cursor = u.cursor()

b = sqlite3.connect('bigrams.db')
b_cursor = b.cursor()

t = sqlite3.connect('trigrams.db')
t_cursor = t.cursor()


def read_data():
    with open(os.path.join('..', 'tests', 'data_to_add.csv'), 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list()
        for row in reader:
            doc = ''.join(row).split(';')
            data.append({'text': doc[0], 'tonal': doc[1]})

        return data


def lemmatization_all_data(data):
    print('lemmatization...')
    with progressbar.ProgressBar(max_value=len(data)) as bar:
        for n in range(len(data)):
            data[n]['text'] = lemmatization(data[n]['text'])
            bar.update(n)

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

    return data


def delta_tf_idf_count(text):
    doc = Document(text)
    doc.count_weight_by_unigrams()
    doc.count_weight_by_bigrams()
    doc.count_weight_by_trigrams()

    return doc.unigrams_weight, doc.bigrams_weight, doc.trigrams_weight


data = lemmatization_all_data(read_data())

os.remove('dataset_with_unigrams_copy.csv')
os.remove('dataset_with_bigrams_copy.csv')
os.remove('dataset_with_trigrams_copy.csv')
