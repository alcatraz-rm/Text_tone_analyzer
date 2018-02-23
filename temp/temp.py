import csv
from pprint import pprint
from modules.lemmatization.lemmatization import lemmatization
import sqlite3
from datetime import datetime


# conn = sqlite3.connect('unigrams.db')
# cursor = conn.cursor()
# changes_date = str(datetime.now())


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


# def check_word(text):
#     request = ("""
#     SELECT * FROM 'data' WHERE Unigram='%s'
#     """) % text
#
#     cursor.execute(request)
#     data = cursor.fetchone()
#     if data:
#         return True
#     else:
#         return False


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

