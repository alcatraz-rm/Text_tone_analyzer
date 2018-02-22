import csv
from pprint import pprint
from modules.lemmatization.lemmatization import lemmatization


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
