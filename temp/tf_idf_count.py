# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


from modules.get_ngram_info.get_ngram_info import get_ngram_info
import math
from modules.count_text_tonal.count_text_tonal import Document
from pprint import pprint

docs_count = 103582  # hardcode


def tf_idf_count(text):
    doc = Document(text)
    tf_text = dict()
    idf_text = dict()
    tf_idf_text = dict()
    checked_unigrams = list()

    # TF count
    for word in doc.unigrams:
        tf_text[word] = doc.unigrams.count(word) / len(doc.unigrams)
        checked_unigrams.append(word)

    # IDF count
    for word in doc.unigrams:
        data = get_ngram_info(word)

        try:
            idf_text[word] = math.log10(docs_count / (data[0] + data[1]))
        except ZeroDivisionError:
            idf_text[word] = 0

    # TF-IDF count
    for word in doc.unigrams:
        tf_idf_text[word] = tf_text[word] * idf_text[word]

    return tf_idf_text


pprint(tf_idf_count(input('text: ')))
