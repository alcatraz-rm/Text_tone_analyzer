import math
import pymorphy2
from pprint import pprint


def lemmatization(string):
    morph = pymorphy2.MorphAnalyzer()

    punctuation_list = ['.', ',', '?', '!', ':', ';', '/', '&', '*', '%', '@', '#', '+', '=', '>', '<', '{', '}', '[',
                        ']', '"', "'", '`',
                        '$', '№', '^', '(', ')']

    for punctuation in punctuation_list:
        string = string.replace(punctuation, '')

    string = string.split()
    for num, word in enumerate(string):
        string[num] = morph.parse(word)[0].normal_form

    string = [word + ' ' for word in string]

    return ''.join(string).strip().lower()


with open('negative (beta).txt') as file:
    negative = [lemmatization(string) for string in file.read().strip().split('\n')]

with open('positive (beta).txt') as file:
    positive = [lemmatization(string) for string in file.read().strip().split('\n')]


def delta_tf_idf(word):
    morph = pymorphy2.MorphAnalyzer()
    word = morph.parse(word)[0].normal_form
    neg_docs = len(negative)
    pos_docs = len(positive)
    pos_docs_word = 1
    neg_docs_word = 1
    this_doc_word = 1

    for string in positive:
        count = string.count(word)
        if count > 0:
            pos_docs_word += 1

    for string in negative:
        count = string.count(word)
        if count > 0:
            neg_docs_word += 1

    print(neg_docs)
    print(pos_docs)
    print(neg_docs_word)
    print(pos_docs_word)

    try:
        v = this_doc_word * math.log10((neg_docs * pos_docs_word) / (pos_docs * neg_docs_word))
    except:
        return 'Error'

    tonal = None
    if v < 0:
        tonal = 'Negative'
    elif v > 0:
        tonal = 'Positive'

    return v, tonal


word = input('Enter the word: ')
v, tonal = delta_tf_idf(word.strip().lower())
print('delta TF-IDF: ', v)
print('Tonal: ', tonal)
