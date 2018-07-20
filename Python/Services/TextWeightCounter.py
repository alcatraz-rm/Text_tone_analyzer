# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


# def unigrams_tf_idf_count(self):
#     tf_text = dict()
#     idf_text = dict()
#     checked_unigrams = list()
#
#     for word in self.unigrams:
#         tf_text[word] = self.unigrams.count(word) / len(self.unigrams)
#         checked_unigrams.append(word)
#
#     for word in self.unigrams:
#         data = self.database_cursor.get_info(word)
#
#         try:
#             idf_text[word] = math.log10(unigrams_docs_count / (data[0] + data[1]))
#         except ZeroDivisionError:
#             idf_text[word] = 0
#
#     for word in self.unigrams:
#         self.unigrams_tf_idf[word] = tf_text[word] * idf_text[word]
#
#
# def bigrams_tf_idf_count(self):
#     tf_text = dict()
#     idf_text = dict()
#     checked_bigrams = list()
#
#     for bigram in self.bigrams:
#         tf_text[bigram] = self.bigrams.count(bigram) / len(self.bigrams)
#         checked_bigrams.append(bigram)
#
#     for bigram in self.bigrams:
#         data = self.database_cursor.get_info(bigram)
#
#         try:
#             idf_text[bigram] = math.log10(unigrams_docs_count / (data[0] + data[1]))
#         except ZeroDivisionError:
#             idf_text[bigram] = 0
#
#     for bigram in self.bigrams:
#         self.bigrams_tf_idf[bigram] = tf_text[bigram] * idf_text[bigram]
#
#
# def trigrams_tf_idf_count(self):
#     tf_text = dict()
#     idf_text = dict()
#     checked_trigrams = list()
#
#     for trigram in self.trigrams:
#         tf_text[trigram] = self.trigrams.count(trigram) / len(self.trigrams)
#         checked_trigrams.append(trigram)
#
#     for trigram in self.trigrams:
#         data = self.database_cursor.get_info(trigram)
#
#         try:
#             idf_text[trigram] = math.log10(unigrams_docs_count / (data[0] + data[1]))
#         except ZeroDivisionError:
#             idf_text[trigram] = 0
#
#     for trigram in self.trigrams:
#         self.trigrams_tf_idf[trigram] = tf_text[trigram] * idf_text[trigram]
#
#
#     def count_ngram_weight(self, ngram):
#         pos_docs = None
#         neg_docs = None
#
#         if ngram.count(' ') == 0:
#             pos_docs = unigrams_pos_docs
#             neg_docs = unigrams_neg_docs
#         elif ngram.count(' ') == 1:
#             pos_docs = unigrams_pos_docs
#             neg_docs = unigrams_neg_docs
#         elif ngram.count(' ') == 2:
#             pos_docs = unigrams_pos_docs
#             neg_docs = unigrams_neg_docs
#
#         pos_docs_word, neg_docs_word, neu_docs_word = self.database_cursor.get_info(ngram)
#
#         if (not (pos_docs_word and neg_docs_word)) or (pos_docs_word == 1 and neg_docs_word == 1):
#             return 0
#
#         delta_tf_idf = math.log10((neg_docs * pos_docs_word) / (pos_docs * neg_docs_word))
#
#         return delta_tf_idf
#
#     def count_weight_by_unigrams_tf_idf(self):
#         checked_unigrams = list()
#         important_unigrams = list()
#
#         for unigram in self.unigrams:
#             if unigram not in checked_unigrams:
#                 unigram_weight = self.unigrams_tf_idf[unigram] * self.count_ngram_weight(unigram)
#                 self.unigrams_weight_tf_idf += unigram_weight
#                 checked_unigrams.append(unigram)
#
#                 if unigram_weight:
#                     important_unigrams.append(unigram)
#
#         if len(important_unigrams) >= round(len(self.unigrams) * 0.6) and important_unigrams:
#             self.unigrams_weight_tf_idf = self.unigrams_weight_tf_idf / len(important_unigrams)
#
#         else:
#             self.unigrams_weight_tf_idf = None
#
#     def count_weight_by_unigrams(self):
#         checked_unigrams = list()
#         important_unigrams = list()
#
#         for unigram in self.unigrams:
#             if unigram not in checked_unigrams:
#                 this_doc_unigram = self.unigrams.count(unigram)
#                 unigram_weight = this_doc_unigram * self.count_ngram_weight(unigram)
#                 self.unigrams_weight += unigram_weight
#                 checked_unigrams.append(unigram)
#
#                 if unigram_weight:
#                     important_unigrams.append(unigram)
#
#         if len(important_unigrams) >= round(len(self.unigrams) * 0.6) and important_unigrams:
#             self.unigrams_weight = self.unigrams_weight / len(important_unigrams)
#
#         else:
#             self.unigrams_weight = None
#
#     def count_weight_by_bigrams_tf_idf(self):
#         if len(self.unigrams) >= 2:
#             checked_bigrams = list()
#             important_bigrams = list()
#
#             for bigram in self.bigrams:
#                 if bigram not in checked_bigrams:
#                     bigram_weight = self.bigrams_tf_idf[bigram] * self.count_ngram_weight(bigram)
#                     self.bigrams_weight_tf_idf += bigram_weight
#                     checked_bigrams.append(bigram)
#
#                     if bigram_weight:
#                         important_bigrams.append(bigram)
#
#             if len(important_bigrams) >= len(self.bigrams) // 2 and important_bigrams:
#                 self.bigrams_weight_tf_idf = self.bigrams_weight_tf_idf / len(important_bigrams)
#
#             else:
#                 self.bigrams_weight_tf_idf = None
#
#     def count_weight_by_bigrams(self):
#         if len(self.unigrams) >= 2:
#             checked_bigrams = list()
#             important_bigrams = list()
#
#             for bigram in self.bigrams:
#                 if bigram not in checked_bigrams:
#                     this_doc_bigram = self.bigrams.count(bigram)
#                     bigram_weight = this_doc_bigram * self.count_ngram_weight(bigram)
#                     self.bigrams_weight += bigram_weight
#                     checked_bigrams.append(bigram)
#
#                     if bigram_weight:
#                         important_bigrams.append(bigram)
#
#             if len(important_bigrams) >= len(self.bigrams) // 2 and important_bigrams:
#                 self.bigrams_weight = self.bigrams_weight / len(important_bigrams)
#
#             else:
#                 self.bigrams_weight = None
#
#     def count_weight_by_trigrams_tf_idf(self):
#         if len(self.unigrams) >= 3:
#             checked_trigrams = list()
#             important_trigrams = list()
#
#             for trigram in self.trigrams:
#                 if trigram not in checked_trigrams:
#                     trigram_weight = self.trigrams_tf_idf[trigram] * self.count_ngram_weight(trigram)
#                     self.trigrams_weight_tf_idf += trigram_weight
#                     checked_trigrams.append(trigram)
#
#                     if trigram_weight:
#                         important_trigrams.append(trigram)
#
#             if len(important_trigrams) >= round(len(self.trigrams) * 0.4) and important_trigrams:
#                 self.trigrams_weight_tf_idf = self.trigrams_weight_tf_idf / len(important_trigrams)
#
#             else:
#                 self.trigrams_weight_tf_idf = None
#
#     def count_weight_by_trigrams(self):
#         if len(self.unigrams) >= 3:
#             checked_trigrams = list()
#             important_trigrams = list()
#
#             for trigram in self.trigrams:
#                 if trigram not in checked_trigrams:
#                     this_doc_trigram = self.trigrams.count(trigram)
#                     trigram_weight = this_doc_trigram * self.count_ngram_weight(trigram)
#                     self.trigrams_weight += trigram_weight
#                     checked_trigrams.append(trigram)
#
#                     if trigram_weight:
#                         important_trigrams.append(trigram)
#
#             if len(important_trigrams) >= round(len(self.trigrams) * 0.4) and important_trigrams:
#                 self.trigrams_weight = self.trigrams_weight / len(important_trigrams)
#
#             else:
#                 self.trigrams_weight = None


class TextWeightCounter:
    def __init__(self):
        pass
