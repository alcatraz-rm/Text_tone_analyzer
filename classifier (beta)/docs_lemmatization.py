import lemmatization
import os


def backup(filename, data):
    path = os.path.join('backup', filename + '_copy' + '.txt')
    with open(path, 'w') as file:
        file.write(data)


def docs_lemmatization(filename):
    data_full = ''
    with open(filename + '.txt', 'r') as file:
        data = file.read().split('\n')

    data = [lemmatization.lemmatization(doc) for doc in data]

    with open(filename + '.txt', 'w') as file:
        for doc in data:
            doc_tmp = doc + '\n'
            file.write(doc_tmp)
            data_full += doc_tmp

    backup(filename, data_full)


docs_lemmatization('negative (beta)')
docs_lemmatization('positive (beta)')
