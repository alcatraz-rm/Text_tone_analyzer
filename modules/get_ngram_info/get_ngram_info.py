# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


import sqlite3
import logging
import os
import warnings
import pymorphy2
from pprint import pprint
import re
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim


def part_of_speech_detect(word):
    part_of_speech = pymorphy2.MorphAnalyzer().parse(word)[0].tag.POS

    if re.match(r'ADJ', part_of_speech):
        return 'ADJ'

    elif re.match(r'PRT', part_of_speech):
        return 'PRT'

    elif part_of_speech == 'INFN':
        return 'VERB'

    elif part_of_speech == 'ADVB':
        return 'ADV'


def nearest_synonym_find(word, vec_model):
    nearest_synonyms = list()
    word = word + '_%s' % part_of_speech_detect(word)

    if word in vec_model:
        for word in vec_model.most_similar(positive=[word], topn=20):
            nearest_synonyms.append({'word': word[0].split('_')[0], 'cosine proximity': word[1]})

    return nearest_synonyms


def relevant_ngram_find(ngram, vec_model):
    nearest_synonyms = nearest_synonym_find(ngram, vec_model)
    pprint(nearest_synonyms)
    conn = sqlite3.connect(os.path.join('..', 'databases', 'unigrams.db'))
    cursor = conn.cursor()

    for synonym in nearest_synonyms:
        cursor.execute("""
        SELECT * FROM 'Data' WHERE Ngram='%s'
        """ % synonym['word'])

        data = cursor.fetchone()
        if data:
            return synonym, data[1], data[2]

    return None, None, None


def get_ngram_info(ngram, vec_model):
    logging.info('\n\nget_ngram_info\n')
    logging.info('start ngram: %s' % ngram)

    if ngram.count(' ') == 0:
        conn = sqlite3.connect(os.path.join('..', 'databases', 'unigrams.db'))
        cursor = conn.cursor()
        logging.info('ngram-type: unigram')

    elif ngram.count(' ') == 1:
        conn = sqlite3.connect(os.path.join('..', 'databases', 'bigrams.db'))
        cursor = conn.cursor()
        logging.info('ngram-type: bigram')

    elif ngram.count(' ') == 2:
        conn = sqlite3.connect(os.path.join('..', 'databases', 'trigrams.db'))
        cursor = conn.cursor()
        logging.info('ngram-type: trigram')

    else:
        logging.error('get empty string')
        return None

    request = ("""
    SELECT * FROM 'Data' WHERE Ngram='%s'
    """) % ngram

    try:
        cursor.execute(request)
        logging.info('request: ok')

    except sqlite3.DatabaseError or sqlite3.DataError:
        logging.error('request: database error')
        return None

    data = cursor.fetchone()
    if data:
        logging.info('received information: %s\n' % str(data))
        return data[1], data[2]  # pos and neg count

    else:
        logging.info('received information: %s\n' % 'none')

        if ngram.count(' ') == 0:
            logging.info('trying to find synonyms...\n')

            nearest_synonym, pos_count, neg_count = relevant_ngram_find(ngram, vec_model)
            if nearest_synonym:
                logging.info('nearest synonym: %s\n' % nearest_synonym['word'])
                logging.info('cosine proximity: %s\n' % nearest_synonym['cosine proximity'])

                return pos_count, neg_count

            else:
                logging.error('can not nearest synonym find\n')

        return 0, 0  # pos and neg count
