# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


import sqlite3
import logging
import os
import pymorphy2
import re

cwd = os.getcwd()


def part_of_speech_detect(word):
    part_of_speech = pymorphy2.MorphAnalyzer().parse(word)[0].tag.POS

    if part_of_speech:
        if re.match(r'ADJ', part_of_speech):
            return 'ADJ'

        elif re.match(r'PRT', part_of_speech):
            return 'PRT'

        elif part_of_speech == 'INFN':
            return 'VERB'

        elif part_of_speech == 'ADVB':
            return 'ADV'


def nearest_synonyms_find(word, vec_model, topn):
    nearest_synonyms = list()
    part_of_speech = part_of_speech_detect(word)
    if part_of_speech:
        word = word + '_%s' % part_of_speech_detect(word)

        if word in vec_model:
            for word in vec_model.most_similar(positive=[word], topn=topn):
                nearest_synonyms.append({'word': word[0].split('_')[0], 'cosine proximity': word[1]})

        return nearest_synonyms
    else:
        logging.info('\ncan not part of speech detect: %s\n' % word)


def by_factor_key(obj):  # func for sorting
    return obj.factor


def relevant_ngram_find(ngram, vec_model):
    if ngram.count(' ') == 0:
        conn = None
        if cwd.endswith('master') or cwd.endswith('temp'):
            conn = sqlite3.connect(os.path.join('..', 'databases', 'unigrams.db'))
        elif cwd.endswith('main'):
            conn = sqlite3.connect(os.path.join('..', '..', '..', 'databases', 'unigrams.db'))

        cursor = conn.cursor()
        nearest_synonyms = nearest_synonyms_find(ngram, vec_model, topn=10)

        for synonym in nearest_synonyms:
            cursor.execute("""
            SELECT * FROM 'Data' WHERE Ngram='%s'
            """ % synonym['word'])

            data = cursor.fetchone()
            if data:
                return synonym, data[1], data[2], data[3]

    elif ngram.count(' ') == 1:
        conn = None
        if cwd.endswith('master') or cwd.endswith('temp'):
            conn = sqlite3.connect(os.path.join('..', 'databases', 'bigrams.db'))
        elif cwd.endswith('main'):
            conn = sqlite3.connect(os.path.join('..', '..', '..', 'databases', 'bigrams.db'))
        cursor = conn.cursor()

        words = ngram.split()
        variants = list()

        words_synonyms = [{'word': words[0], 'synonyms': nearest_synonyms_find(words[0], vec_model, topn=3)},
                          {'word': words[1], 'synonyms': nearest_synonyms_find(words[1], vec_model, topn=3)}]

        if not words_synonyms[0]['synonyms']:
            words_synonyms[0]['synonyms'].append(words_synonyms[0]['word'])

        if not words_synonyms[1]['synonyms']:
            words_synonyms[1]['synonyms'].append(words_synonyms[1]['word'])

        for first_word in words_synonyms[0]['synonyms']:
            for second_word in words_synonyms[1]['synonyms']:
                variants.append({'bigram': first_word['word'] + ' ' + second_word['word'],
                                 'factor': first_word['cosine proximity'] + second_word['cosine proximity']})

        for variant in variants:
            cursor.execute("""
            SELECT * FROM 'Data' WHERE Ngram='%s'
            """ % variant['bigram'])

            data = cursor.fetchone()
            if data:
                return variant['bigram'], data[1], data[2], data[3]

    return None, None, None, None


def get_ngram_info(ngram, vec_model):
    logging.info('\n\nget_ngram_info\n')
    logging.info('start ngram: %s' % ngram)
    conn = None

    if ngram.count(' ') == 0:
        if cwd.endswith('master') or cwd.endswith('temp'):
            conn = sqlite3.connect(os.path.join('..', 'databases', 'unigrams.db'))
        elif cwd.endswith('main'):
            conn = sqlite3.connect(os.path.join('..', '..', '..', 'databases', 'unigrams.db'))

        cursor = conn.cursor()
        logging.info('ngram-type: unigram')

    elif ngram.count(' ') == 1:
        if cwd.endswith('master') or cwd.endswith('temp'):
            conn = sqlite3.connect(os.path.join('..', 'databases', 'bigrams.db'))
        elif cwd.endswith('main'):
            conn = sqlite3.connect(os.path.join('..', '..', '..', 'databases', 'bigrams.db'))

        cursor = conn.cursor()
        logging.info('ngram-type: bigram')

    elif ngram.count(' ') == 2:
        if cwd.endswith('master') or cwd.endswith('temp'):
            conn = sqlite3.connect(os.path.join('..', 'databases', 'trigrams.db'))
        elif cwd.endswith('main'):
            conn = sqlite3.connect(os.path.join('..', '..', '..', 'databases', 'trigrams.db'))

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
        return data[1], data[2], data[3]  # pos and neg count

    else:
        logging.info('received information: %s\n' % 'none')

        if ngram.count(' ') == 0:
            logging.info('trying to find synonyms...\n')

            nearest_synonym, pos_count, neg_count, neu_count = relevant_ngram_find(ngram, vec_model)

            if nearest_synonym:
                logging.info('nearest synonym: %s\n' % nearest_synonym['word'])
                logging.info('cosine proximity: %s\n' % nearest_synonym['cosine proximity'])

                return pos_count, neg_count, neu_count

            else:
                logging.error('can not nearest synonym find\n')

        if ngram.count(' ') == 1:
            logging.info('trying to find synonyms...\n')

            bigram, pos_count, neg_count, neu_count = relevant_ngram_find(ngram, vec_model)

            if bigram:
                logging.info('nearest bigram: %s\n' % bigram)
            else:
                logging.error('can not nearest bigram find\n')

        return 0, 0, 0  # pos, neg and neu count
