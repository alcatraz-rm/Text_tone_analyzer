from modules.get_word_info.get_word_info import get_word_info
import math


def delta_tf_idf(word, this_doc_word):
    pos_docs = 45577
    neg_docs = 53750
    pos_docs_word, neg_docs_word = get_word_info(word)
    if pos_docs_word == 0 and neg_docs_word == 0:
        return 0

    if pos_docs_word == 0:
        pos_docs_word = 1
    if neg_docs_word == 0:
        neg_docs_word = 1

    return this_doc_word * math.log10((neg_docs * pos_docs_word) / (pos_docs * neg_docs_word))


def count_text_weight(text):
    text = text.split()
    text_weight = 0

    for word in text:
        this_doc_word = text.count(word)
        word_weight = delta_tf_idf(word, this_doc_word)
        text_weight += word_weight

    return text_weight/len(text)
