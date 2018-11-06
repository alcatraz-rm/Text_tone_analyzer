import csv
import os

from Python.Services.PathService import PathService

path_service = PathService()


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


def split(dataset):
    print(len(dataset))

    previous_index = 0
    current_index = 0
    parts_count = len(dataset) // 10000
    parts = list()

    for i in range(1, parts_count):
        current_index = i * 10000

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

