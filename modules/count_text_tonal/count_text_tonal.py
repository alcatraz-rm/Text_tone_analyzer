# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

from modules.count_text_weight.count_text_weight import count_text_weight
from modules.lemmatization.lemmatization import lemmatization
from modules.classifier.classifier import classifier
from modules.get_ngram_info.get_ngram_info import get_ngram_info
import math


class Document:
    def __init__(self, text):
        self.text = text
        self.unigrams = text.split()
        self.bigrams = list()
        self.trigrams = list()
        self.unigrams_weight = 0
        self.bigrams_weight = 0
        self.trigrams_weight = 0
        self.tonal = 'Unknown'

    def split_into_bigrams(self):
        for unigram_index in range(len(self.unigrams) - 1):
            self.bigrams.append(self.unigrams[unigram_index] + ' ' + self.unigrams[unigram_index + 1])

    def split_into_trigrams(self):
        for unigram_index in range(len(self.unigrams) - 2):
            self.trigrams.append(self.unigrams[unigram_index] + ' ' + self.unigrams[unigram_index + 1] + ' ' \
                                + self.unigrams[unigram_index + 2])

    def count_unigram_weight(self, unigram):
        pos_docs = 45577
        neg_docs = 53750
        pos_docs_word, neg_docs_word = get_ngram_info(unigram)
        if pos_docs_word == 0 and neg_docs_word == 0:
            return 0

        if pos_docs_word == 0:
            pos_docs_word = 1
        if neg_docs_word == 0:
            neg_docs_word = 1

        return math.log10((neg_docs * pos_docs_word) / (pos_docs * neg_docs_word))

    def count_weight_by_unigrams(self):
        checked_unigrams = list()

        for unigram in self.unigrams:
            if unigram not in checked_unigrams:
                this_doc_unigram = self.unigrams.count(unigram)
                word_weight = this_doc_unigram * self.count_unigram_weight(unigram)
                self.unigrams_weight += word_weight
                checked_unigrams.append(unigram)

        if len(self.unigrams) != 0:
            self.unigrams_weight = self.unigrams_weight / len(checked_unigrams)
        else:
            self.unigrams_weight = 0


def count_text_tonal(text):
    text = lemmatization(text)
    doc = Document(text)
    doc.count_weight_by_unigrams()
    print(doc.unigrams_weight)
    # weight = count_text_weight(text)
    if doc.unigrams_weight == 0:
        tonal = 'Unknown Tonal'
    else:
        tonal = classifier(doc.unigrams_weight)

    return tonal, doc.unigrams_weight
