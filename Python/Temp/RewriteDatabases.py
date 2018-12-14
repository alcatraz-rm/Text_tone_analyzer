# Copyright © 2018. All rights reserved.
# Author: German Yakimov

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv
import os
import re
import json
import time

from Python.Services.Lemmatizer.Lemmatizer import Lemmatizer
from Python.Services.PathService import PathService

path_service = PathService()
lemmatizer = Lemmatizer()


def get_dataset(name):
    path = path_service.get_path_to_dataset(name)

    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        data = [row[0].split(';')[0] for row in reader if row]
        del (data[0])

        return data


def dump_dataset(data):
    with open('dataset.csv', 'w', encoding='utf-8') as file:
        for text in data:
            file.write(text + '\n')


def read_dataset():
    with open('dataset.csv') as file:
        reader = csv.reader(file)

        return [row[0] for row in reader]


def split_dataset(dataset):
    part_size = 1000
    print(len(dataset))

    previous_index = 0
    parts_count = len(dataset) // part_size
    parts = list()

    for i in range(1, parts_count):
        current_index = i * part_size

        parts.append(dataset[previous_index:current_index])
        previous_index = current_index

    parts.append(dataset[previous_index:])
    print(sum([len(part) for part in parts]))
    print(len(parts))

    return parts


def dump_parts(parts):
    for n, part in enumerate(parts):
        with open(os.path.join('lemmatized_parts', f'part_{n}.csv'), 'w', encoding='utf-8') as file:
            for text in part:
                file.write(text + '\n')


def dump_part(lemmatized_part, number):
    with open(os.path.join('parts', 'lemmatized', f'part_{number}.csv'), 'w', encoding='utf-8') as file:
        for text in lemmatized_part:
            if text:
                file.write(text + '\n')


def lemmatize_part(part):
    data = list()
    lemmatized_data = list()

    with open(os.path.join('parts', 'start', f'part_{part}.csv'), 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            data.append(row[0])

    for n, text in enumerate(data):
        lemmatized_data.append(lemmatizer.get_text_initial_form(text))
        print(n)

    dump_part(lemmatized_data, part)
    print(len(lemmatized_data))


def merge_all_lemmatized_parts():
    path_to_parts = os.path.join('parts', 'lemmatized')

    with open('dataset_lemmatized.csv', 'w', encoding='utf-8') as dt:
        for part in os.listdir(path_to_parts):
            with open(os.path.join(path_to_parts, part), 'r', encoding='utf-8') as file:
                reader = csv.reader(file)

                for row in reader:
                    dt.write(row[0] + '\n')


def split_into_unigrams(text: str):
    if text:
        return re.findall(r'\w+', text)


def split_into_bigrams(text: str):
    if not text:
        return

    unigrams = split_into_unigrams(text)
    bigrams = list()

    if len(unigrams) >= 2:
        for unigram_index in range(len(unigrams) - 1):
            bigram = ' '.join(sorted([unigrams[unigram_index], unigrams[unigram_index + 1]])).strip()
            bigrams.append(bigram)

        return bigrams


def split_into_trigrams(text: str):
    if not text:
        return

    unigrams = split_into_unigrams(text)
    trigrams = list()

    if len(unigrams) >= 3:
        for unigram_index in range(len(unigrams) - 2):
            trigram = ' '.join(sorted(
                [unigrams[unigram_index],
                 unigrams[unigram_index + 1],
                 unigrams[unigram_index + 2]])).strip()

            trigrams.append(trigram)

        return trigrams


def split_dataset_into_ngrams():
    unigrams = set()
    bigrams = set()
    trigrams = set()

    with open('dataset_lemmatized.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            text = row[0]

            if text:
                unigrams.update(set(split_into_unigrams(text)) if text else list())

                if len(text.split()) > 1:
                    bigrams.update(set(split_into_bigrams(text)) if text else list())

                    if len(text.split()) > 2:
                        trigrams.update(set(split_into_trigrams(text)) if text else list())

    return unigrams, bigrams, trigrams


def dump_ngrams(unigrams, bigrams, trigrams):
    with open('unigrams.csv', 'w', encoding='utf-8') as file:
        for unigram in unigrams:
            file.write(unigram + '\n')

    with open('bigrams.csv', 'w', encoding='utf-8') as file:
        for bigram in bigrams:
            file.write(bigram + '\n')

    with open('trigrams.csv', 'w', encoding='utf-8') as file:
        for trigram in trigrams:
            file.write(trigram + '\n')


def count_ngrams(ngrams, part_number):
    with open(os.path.join('lemmatized_parts', f'part_{part_number}.csv'), 'r',
              encoding='utf-8') as file:
        reader = csv.reader(file)

        texts = [row[0] for row in reader]

    unigrams, bigrams, trigrams = list(), list(), list()

    for text in texts:
        if text:
            unigrams = set(split_into_unigrams(text)) if text else list()

            if len(text.split()) > 1:
                bigrams = set(split_into_bigrams(text)) if text else list()

                if len(text.split()) > 2:
                    trigrams = set(split_into_trigrams(text)) if text else list()

    for unigram in unigrams:
        if unigram in ngrams['unigrams']:
            ngrams['unigrams'][unigram] += 1
        else:
            ngrams['unigrams'][unigram] = 1

    for bigram in bigrams:
        if bigram in ngrams['bigrams']:
            ngrams['bigrams'][bigram] += 1
        else:
            ngrams['bigrams'][bigram] = 1

    for trigram in trigrams:
        if trigram in ngrams['trigrams']:
            ngrams['trigrams'][trigram] += 1
        else:
            ngrams['trigrams'][trigram] = 1

    return ngrams


def continue_counting():
    with open('ngrams.json', 'r', encoding='utf-8') as file:
        ngrams = json.load(file)

    last_part = ngrams['last_part'] + 1

    for part in range(last_part, 103):
        ngrams = count_ngrams(ngrams, part)
        ngrams['last_part'] = part

        print('part: %d' % part)

        if part == 102:
            with open('ngrams.json', 'w', encoding='utf-8') as file:
                json.dump(ngrams, file, indent=4, ensure_ascii=False)
            exit(0)


with open('ngrams.json', 'w', encoding='utf-8') as file:
    json.dump(dict(unigrams=dict(), bigrams=dict(), trigrams=dict(),
                   last_part=0), file)

continue_counting()

