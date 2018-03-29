import csv
from pprint import pprint
from modules.count_text_tonal.count_text_tonal import Document
import json


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
    for n in range(len(data)):
        data[n] = count_weights(data[n])

    return data


data = read_dataset()
data = append_weights(data)

with open('dataset_rewrited.json', 'w', encoding='utf-8') as file:
    json.dump(obj=data, fp=file, indent=4)
