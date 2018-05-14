import sqlite3
import csv
import os
import progressbar
from pprint import pprint
from modules.lemmatization.lemmatization import lemmatization
from modules.get_ngram_info.get_ngram_info import get_ngram_info


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


def split_ngrams_by_status(unigrams, bigrams, trigrams):
    print('\nsplitting N-grams by database status...')
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

    return new_unigrams, new_bigrams, new_trigrams


# data = lemmatization_all_data(read_data())
# unigrams, bigrams, trigrams = split_ngrams_by_status(*split_into_ngrams(data))
