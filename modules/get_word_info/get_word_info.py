import sqlite3
import pymorphy2


def get_word_info(word):
    conn = sqlite3.connect('words_database.db')
    cursor = conn.cursor()
    morph = pymorphy2.MorphAnalyzer()

    word = morph.parse(word)[0].normal_form

    request = ("""
    SELECT * FROM 'Words' WHERE Word='%s'
    """) % word

    cursor.execute(request)
    data = cursor.fetchone()
    if data:
        pos_count = data[1]
        neg_count = data[2]
    else:
        pos_count = 0
        neg_count = 0

    return pos_count, neg_count
