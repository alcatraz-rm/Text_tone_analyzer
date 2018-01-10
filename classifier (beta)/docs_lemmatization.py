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
        length = len(data)

    data = [lemmatization.lemmatization(doc) for doc in data]

    with open(filename + '.txt', 'w') as file:
        for doc in data:
            doc_tmp = doc + '\n'
            data_full += doc_tmp
        data_full = data_full.strip()
        file.write(data_full)

    backup(filename, data_full)

    return length


def length_update(pos_len, neg_len):
    print('Positive Documents - %d' % pos_len)
    print('Negative Documents - %d' % neg_len)

    with open('docs_count.txt', 'w') as file:
        file.write(str(pos_len) + '\n')
        file.write(str(neg_len))


neg_len = docs_lemmatization('negative (beta)')
pos_len = docs_lemmatization('positive (beta)')
length_update(pos_len, neg_len)
