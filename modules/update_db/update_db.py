import sqlite3
from datetime import datetime


conn = sqlite3.connect('words_database.db')
cursor = conn.cursor()
changes_date = str(datetime.now())

with open('positive (base).txt', 'r', encoding='utf-8') as file:
    positive = file.read().split('\n')

with open('negative (base).txt', 'r', encoding='utf-8') as file:
    negative = file.read().split('\n')


def pos_and_neg_docs_count(word):
    pos_count = 0
    neg_count = 0

    for doc in positive:
        if word in doc:
            pos_count += 1
    for doc in negative:
        if word in doc:
            neg_count += 1

    return pos_count, neg_count


def check_entry(word):
    cursor.execute("""SELECT * FROM Words""")
    rows = cursor.fetchall()
    words = list()
    for entry in rows:
        words.append(entry[0])

    if word in words:
        return True
    else:
        return False


def add_word_to_db(word):
    if not word.isdigit():
        pos_count, neg_count = pos_and_neg_docs_count(word)
        cursor.execute("""
        INSERT INTO Words
        VALUES ('%s', %d, %d, '%s')""" % (word, pos_count, neg_count, changes_date))
        conn.commit()


def update_word(word):
    if word.isdigit():
        cursor.execute("""DELETE FROM Words WHERE Word = '%s'""" % word)
    else:
        request = ("""
        SELECT * FROM Words WHERE Word='%s'
        """) % word

        cursor.execute(request)
        data = cursor.fetchone()

        if data[3] != changes_date:
            pos_count, neg_count = pos_and_neg_docs_count(word)
            cursor.execute("""
            UPDATE Words
            SET Pos_count = %d
            WHERE Word = '%s'
            """ % (pos_count, word))

            cursor.execute("""
            UPDATE Words
            SET Neg_count = %d
            WHERE Word = '%s'
            """ % (neg_count, word))

            cursor.execute("""
            UPDATE Words
            SET Changes_Date = '%s'
            WHERE Word = '%s'
            """ % (changes_date, word))

            conn.commit()


def update_db():
    conn = sqlite3.connect('words_database.db')
    cursor = conn.cursor()

    with open('positive (base).txt', 'r', encoding='utf-8') as file:
        positive = file.read().split('\n')

    with open('negative (base).txt', 'r', encoding='utf-8') as file:
        negative = file.read().split('\n')
    counter = 0
    for doc_text in positive:
        counter += 1
        print(counter)
        doc_words = doc_text.split()

        for word in doc_words:
            if check_entry(word) is True:
                update_word(word)
            else:
                add_word_to_db(word)

        conn.commit()

    counter = 0
    for doc_text in negative:
        counter += 1
        print(counter)
        doc_words = doc_text.split()

        for word in doc_words:
            if check_entry(word) is True:
                update_word(word)
            else:
                add_word_to_db(word)

        conn.commit()

    conn.commit()

    cursor.close()
