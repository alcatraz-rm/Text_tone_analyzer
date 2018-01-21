# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import csv
import copy


class Document:
    def __init__(self, tonal, weight):
        self.tonal = tonal
        self.weight = weight


def by_weight_key(obj):
    return obj.weight


def add_all_docs_to_list():
    line = []

    with open('positive (base)_updated.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for doc in reader:
            doc = ''.join(doc).split(';')
            obj = Document('positive', doc[1])
            line.append(obj)
            line = copy.deepcopy(line)

    with open('negative (base)_updated.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for doc in reader:
            doc = ''.join(doc).split(';')
            obj = Document('negative', doc[1])
            line.append(obj)
            line = copy.deepcopy(line)

    line = sorted(line, key=by_weight_key)

    return line


def get_nearest_neighbour(n_value, n_list):
    left = 0
    right = len(n_list)
    while right - left > 1:
        i = left + (right - left) // 2
        if n_value < n_list[i].weight:
            right = i
        else:
            left = i

    a = min([(abs(n_value - n_list[j].weight), n_list[j].weight, j) for j in (i - 1, i, i + 1)])

    return a[1:3]


def nearest_neighbours_find(k, line, weight):
    neighbours = []

    for i in range(k):
        pos = get_nearest_neighbour(weight, line)[1]
        neighbours.append(line[pos])
        del(line[pos])
        neighbours = copy.deepcopy(neighbours)

    return neighbours


def most_common_class_find(neighbours):
    positive = 0
    negative = 0

    for neighbour in neighbours:
        if neighbour.tonal == 'positive':
            positive += 1
        elif neighbour.tonal == 'negative':
            negative += 1

    if positive > negative:
        return 'positive'
    elif negative > positive:
        return 'negative'
    elif positive == negative:
        return 'neutral'


def classifier(weight):
    document = Document('', weight)
    line = add_all_docs_to_list()
    k = 1000
    neighbours = nearest_neighbours_find(k, line, document.weight)
    document.tonal = most_common_class_find(neighbours)

    return document.tonal
