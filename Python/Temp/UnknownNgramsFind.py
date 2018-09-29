# Copyright © 2018. All rights reserved.
# Author: German Yakimov

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv
import os
from pprint import pprint

from Python.Services.DatabaseCursor import DatabaseCursor
from Python.Services.DocumentPreparer import DocumentPreparer
from Python.Services.Lemmatizer.Lemmatizer import Lemmatizer

ngrams = list()
document_preparer = DocumentPreparer()
lemmatizer = Lemmatizer()
database_cursor = DatabaseCursor()

with open(os.path.join('..', 'Tests', 'tests.csv'), 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        text = lemmatizer.get_text_initial_form(''.join(row).split(';')[0])
        unigrams = document_preparer.split_into_unigrams(text)

        for unigram in unigrams:
            if unigram not in ngrams:
                ngrams.append(unigram)

        if len(unigrams) > 1:
            for bigram in document_preparer.split_into_bigrams(text):
                if bigram not in ngrams:
                    ngrams.append(bigram)

        if len(unigrams) > 2:
            for trigram in document_preparer.split_into_trigrams(text):
                if trigram not in ngrams:
                    ngrams.append(trigram)

unknown_ngrams = list()

for k, ngram in enumerate(ngrams):
    if not database_cursor.entry_exists(ngram):
        unknown_ngrams.append(ngram)
        print(k, 0)
    else:
        print(k, 1)

with open('unknown_unigrams.csv', 'w', encoding='utf-8') as u:
    with open('unknown_bigrams.csv', 'w', encoding='utf-8') as b:
        with open('unknown_trigrams.csv', 'w', encoding='utf-8') as t:

            for unknown_ngram in unknown_ngrams:
                if unknown_ngram.count(' ') == 0:
                    u.write(unknown_ngram + '\n')
                elif unknown_ngram.count(' ') == 1:
                    b.write(unknown_ngram + '\n')
                elif unknown_ngram.count(' ') == 2:
                    t.write(unknown_ngram + '\n')

pprint(unknown_ngrams)
print(len(unknown_ngrams))
