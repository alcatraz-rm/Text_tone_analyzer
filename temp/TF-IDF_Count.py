from modules.get_ngram_info.get_ngram_info import get_ngram_info
import math
from modules.count_text_tonal.count_text_tonal import Document
from pprint import pprint
docs_count = 103582


def tf_idf_count(ngram, text):
    data = get_ngram_info(ngram)
    ngram_tf_idf = text.split().count(ngram) * math.log10(docs_count/(data[0] + data[1]))

    return ngram_tf_idf


unigrams_weight = dict()
doc = Document(input('text: '))
checked_unigrams = list()
for unigram in doc.unigrams:
    if unigram not in checked_unigrams:
        unigrams_weight[unigram] = tf_idf_count(unigram, doc.text)
        checked_unigrams.append(unigram)

pprint(unigrams_weight)
