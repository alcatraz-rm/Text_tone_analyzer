import csv
from pprint import pprint
from modules.lemmatization.lemmatization import lemmatization
import sqlite3
from datetime import datetime
import copy


conn = sqlite3.connect('unigrams.db')
cursor = conn.cursor()
changes_date = str(datetime.now())


pos = list()
with open('positive.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for f in reader:
        pos.append(''.join(f))


neg = list()
with open('negative.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for f in reader:
        neg.append(''.join(f))


neu = list()
with open('neutral.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for f in reader:
        neu.append(''.join(f))


def check_word(text):
    request = ("""
    SELECT * FROM 'data' WHERE Unigram='%s'
    """) % text

    cursor.execute(request)
    data = cursor.fetchone()
    if data:
        return True
    else:
        return False


def count(word):
    word = lemmatization(word)
    pos_count = 1
    neg_count = 1
    neu_count = 1

    for doc in pos:
        if word in doc:
            pos_count += 1

    for doc in neg:
        if word in doc:
            neg_count += 1

    for doc in neu:
        if word in doc:
            neu_count += 1

    return pos_count, neg_count, neu_count


def add_to_db(data):
    cursor.executemany("INSERT INTO [Data] VALUES (?,?,?,?,?)", data)
    conn.commit()


def add_to_data(unigram, data):
    pos, neg, neu = count(unigram)
    data.append((unigram, pos, neg, neu, changes_date))
    data = copy.deepcopy(data)

    return data


with open('neutral.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    k = 0
    data = list()

    for row in reader:
        doc = ''.join(row)
        for unigram in doc.split():
            if not check_word(unigram):
                data = add_to_data(unigram, data)
        k += 1
        print(k)

        if k % 500 == 0:
            add_to_db(data)
            data.clear()

    add_to_db(data)

cursor.close()
