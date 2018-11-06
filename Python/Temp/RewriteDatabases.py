import csv

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


data = get_dataset('dataset_with_unigrams.csv')
dump_dataset(data)
