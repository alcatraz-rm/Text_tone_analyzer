# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


from modules.get_ngram_info.get_ngram_info import get_ngram_info
import math


def delta_tf_idf(word, this_doc_word):
    pos_docs = 45577
    neg_docs = 53750
    pos_docs_word, neg_docs_word = get_ngram_info(word)
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
    checked_words = list()

    for word in text:
        if word not in checked_words:
            this_doc_word = text.count(word)
            word_weight = delta_tf_idf(word, this_doc_word)
            text_weight += word_weight
            checked_words.append(word)

    if len(text) != 0:
        return text_weight/len(text)
    else:
        return 0
