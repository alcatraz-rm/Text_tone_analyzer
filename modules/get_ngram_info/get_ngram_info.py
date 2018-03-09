# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


import sqlite3
import logging
import os


def get_ngram_info(ngram):
    logging.info('\n\nget_ngram_info\n')
    logging.info('start ngram: %s' % ngram)
    logging.info('lemmatized ngram: %s' % ngram)

    if ngram.count(' ') == 0:
        conn = sqlite3.connect('unigrams.db')
        cursor = conn.cursor()
        logging.info('ngram-type: unigram')

    elif ngram.count(' ') == 1:
        conn = sqlite3.connect('bigrams.db')
        cursor = conn.cursor()
        logging.info('ngram-type: bigram')

    elif ngram.count(' ') == 2:
        conn = sqlite3.connect('trigrams.db')
        cursor = conn.cursor()
        logging.info('ngram-type: trigram')

    else:
        logging.error('get empty string')
        return 'error, get empty string'

    request = ("""
    SELECT * FROM 'Data' WHERE Ngram='%s'
    """) % ngram

    try:
        cursor.execute(request)
        logging.info('request: ok')
    except:
        logging.error('request: database lost')
        return 'error: database lost'

    data = cursor.fetchone()
    if data:
        pos_count = data[1]
        neg_count = data[2]
        logging.info('received information: %s\n' % str(data))
    else:
        pos_count = 0
        neg_count = 0
        logging.info('received information: %s\n' % 'none')

    return pos_count, neg_count
