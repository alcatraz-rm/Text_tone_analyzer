from modules.lemmatization.lemmatization import lemmatization
from datetime import datetime


def add_docs_to_db():
    with open('positive-tmp.txt', 'r') as file:
        positive_tmp = [lemmatization(doc) for doc in file.read().split('\n')]

    with open('negative-tmp.txt', 'r') as file:
        negative_tmp = [lemmatization(doc) for doc in file.read().split('\n')]

    with open('positive (base).txt', 'r') as file:
        positive_base = file.read().split('\n')

    with open('negative (base).txt', 'r') as file:
        negative_base = file.read().split('\n')

    positive_docs_count = 0
    negative_docs_count = 0

    with open('positive (base).txt', 'a') as file:
        for doc in positive_tmp:
            if doc not in positive_base:
                file.write(doc + '\n')
                positive_docs_count += 1

    with open('negative (base).txt', 'a') as file:
        for doc in negative_tmp:
            if doc not in negative_base:
                file.write(doc + '\n')
                negative_docs_count += 1

    with open('docs_count.txt', 'w') as file:
        file.write('%d\n' % (len(positive_base) + positive_docs_count))
        file.write('%d\n' % (len(negative_base) + negative_docs_count))
        file.write(str(datetime.now()))

    with open('positive-tmp.txt', 'w') as file:
        file.write('')

    with open('negative-tmp.txt', 'w') as file:
        file.write('')
