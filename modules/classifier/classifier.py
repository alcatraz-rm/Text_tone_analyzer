# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import json


class Document:
    def __init__(self, tonal, weight):
        self.tonal = tonal
        self.weight = weight


def by_weight_key(obj):
    return float(obj.weight)


def add_all_docs_to_list(weight_obj):
    with open('line.json', 'r', encoding='utf-8') as file:
        line = json.load(file)

    line_pos = line['positive']
    line_neg = line['negative']
    line = []

    for weight in line_pos:
        # print(weight)
        line.append(Document('positive', weight))

    for weight in line_neg:
        line.append(Document('negative', weight))

    line.append(Document('unknown', weight_obj))

    line = sorted(line, key=by_weight_key)

    return line


def nearest_neighbours_find(k, line, weight):
    neighbours = []

    for i, elem in enumerate(line):
        if elem.tonal == 'unknown':
            pos = i
            break

    if pos == 0:
        for i in range(k):
            neighbours.append(i)
        return neighbours

    if pos == len(line) - 1:
        i = len(line) - 2
        while i > len(line) - k - 1:
            neighbours.append(i)
            i -= 1
        return neighbours

    right = pos + 1
    left = pos - 1

    for l in range(k):
        try:
            if abs(weight) - abs(line[right].weight) < abs(weight) - abs(line[left].weight):
                neighbours.append(right)
                right += 1
                continue
        except:
            for j in range(k - l):
                neighbours.append(left)
                left -= 1
            break
        try:
            if abs(weight) - abs(line[left].weight) <= abs(weight) - abs(line[right].weight):
                neighbours.append(left)
                left -= 1
                continue
        except:
            for j in range(k - l):
                neighbours.append(right)
                right += 1
            break

    return neighbours


def most_common_class_find(neighbours, line):
    positive = 0
    negative = 0

    for neighbour in neighbours:
        if line[neighbour].tonal == 'positive':
            positive += 1
        elif line[neighbour].tonal == 'negative':
            negative += 1

    if positive > negative:
        return 'positive'
    elif negative > positive:
        return 'negative'
    elif positive == negative:
        return 'neutral'


def classifier(weight):
    weight = float(weight)
    line = add_all_docs_to_list(weight)
    k = 10
    neighbours = nearest_neighbours_find(k, line, weight)
    tonal = most_common_class_find(neighbours, line)

    return tonal
