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
        with open(os.path.join('parts', 'start', f'part_{n}.csv'), 'w', encoding='utf-8') as file:
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
        if n == 1428:
            print('fuck')

        lemmatized_data.append(lemmatizer.get_text_initial_form(text))
        print(n)

    dump_part(lemmatized_data, part)
    print(len(lemmatized_data))


for i in range(103):
    lemmatize_part(i)
    print(i)
    time.sleep(2)
