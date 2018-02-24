# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


import sqlite3
from modules.lemmatization.lemmatization import lemmatization


def get_ngram_info(ngram):
    ngram = lemmatization(ngram)

    if ngram.count(' ') == 0:
        conn = sqlite3.connect('unigrams.db')
        cursor = conn.cursor()

    elif ngram.count(' ') == 1:
        conn = sqlite3.connect('bigrams.db')
        cursor = conn.cursor()

    elif ngram.count(' ') == 2:
        conn = sqlite3.connect('trigrams.db')
        cursor = conn.cursor()
    else:
        return 'Error, get empty string'

    request = ("""
    SELECT * FROM 'Data' WHERE Ngram='%s'
    """) % ngram

    cursor.execute(request)
    data = cursor.fetchone()
    if data:
        pos_count = data[1]
        neg_count = data[2]
    else:
        pos_count = 0
        neg_count = 0

    return pos_count, neg_count
