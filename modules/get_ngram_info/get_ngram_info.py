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
        logging.error('request: database lost')
        return None

    data = cursor.fetchone()
    if data:
        logging.info('received information: %s\n' % str(data))
        return data[1], data[2]  # pos and neg count

    else:
        logging.info('received information: %s\n' % 'none')
        return 0, 0  # pos and neg count
