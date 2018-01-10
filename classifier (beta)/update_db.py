import sqlite3


conn = sqlite3.connect('words_database.db')
cursor = conn.cursor()


with open('positive (beta).txt', 'r') as file:
    positive = file.read().split('\n')

with open('negative (beta).txt', 'r') as file:
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
    pos_count, neg_count = pos_and_neg_docs_count(word)
    cursor.execute("""
    INSERT INTO Words
    VALUES ('%s', %d, %d, 0)""" % (word, pos_count, neg_count))
    conn.commit()


def update_word(word):
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

    conn.commit()


tmp_entry = list()
entries = list()

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

cursor.close()
