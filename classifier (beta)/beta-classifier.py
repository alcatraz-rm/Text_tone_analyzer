import math
import pymorphy2
from modules.get_word_info.get_word_info import get_word_info


def delta_tf_idf(word):
    morph = pymorphy2.MorphAnalyzer()
    word = morph.parse(word)[0].normal_form

    with open('docs_count.txt', 'r') as file:
        data = file.read().split('\n')
        pos_docs = int(data[0])
        neg_docs = int(data[1])

    this_doc_word = 1

    pos_docs_word, neg_docs_word = get_word_info(word)

    if pos_docs_word == 0:
        pos_docs_word = 1
    if neg_docs_word == 0:
        neg_docs_word = 1

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
