# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


import csv
from modules.count_text_tonal.count_text_tonal import Document


def read_dataset():
    with open('dataset.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list()
        for row in reader:
            data.append(''.join(row).split(';'))

    return data


def count_weights(doc):
    doc_obj = Document(doc[0])

    doc_obj.count_weight_by_bigrams()
    doc_obj.count_weight_by_trigrams()

    doc.append(doc_obj.bigrams_weight)
    doc.append(doc_obj.trigrams_weight)

    return doc


def append_weights(data):
    return [count_weights(doc) for doc in data]


data = append_weights(read_dataset())

with open('dataset_rewrited.json', 'w', encoding='utf-8') as file:
    for n, doc in enumerate(data):
        file.write(data[0] + ';' + data[1] + ';' + data[2] + ';' + data[3] + ';' + data[4] + '\n')
        print(n)
