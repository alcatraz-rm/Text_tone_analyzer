import os
import csv
from pprint import pprint
from Python.Services.DocumentPreparer import DocumentPreparer
from Python.Services.Lemmatizer.Lemmatizer import Lemmatizer
from Python.Services.DatabaseCursor import DatabaseCursor


ngrams = list()
document_preparer = DocumentPreparer()
lemmatizer = Lemmatizer()
database_cursor = DatabaseCursor()

with open(os.path.join('..', 'Tests', 'tests.csv'), 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        text = lemmatizer.lead_to_initial_form(''.join(row).split(';')[0])
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

with open('unknown_ngrams.csv', 'w', encoding='utf-8') as file:
    for unknown_ngram in unknown_ngrams:
        file.write(unknown_ngram + '\n')

pprint(unknown_ngrams)
print(len(unknown_ngrams))
