# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


from modules.count_text_tonal.count_text_tonal import Document
import csv
import os
import json
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import unittest

vec_model = gensim.models.KeyedVectors.load_word2vec_format(os.path.join('..', 'databases',
                                                                         'ruscorpora_upos_skipgram_300_10_2017.bin.gz'),
                                                            binary=True)


class TonalTestCase(unittest.TestCase):
    def test(self):
        self.read_cases()
        self.test_results = {'tests': list(), 'passed': 0, 'failed': 0}

        for case, data in self.cases.items():
            with self.subTest(case=case, test=data['text']):
                doc = Document(data['text'], vec_model)
                doc.count_weight_by_unigrams()
                doc.count_weight_by_bigrams()
                doc.classification()
                self.assertEqual(
                    data['expected_tonal'],
                    doc.tonal,
                )

            if doc.tonal == data['expected_tonal']:
                self.test_results['passed'] += 1
                status = 'passed'
            else:
                self.test_results['failed'] += 1
                status = 'failed'

            self.test_results['tests'].append({'text': data['text'], 'case': case, 'result': doc.tonal, 'status': status})

            print(case)

        self.test_results['accuracy'] = str(round(self.test_results['passed'] / len(self.cases), 3) * 100) + '%'

        with open('test_log_negative.json', 'w', encoding='utf-8') as file:
            json.dump(self.test_results, file, indent=4, ensure_ascii=False)

    def read_cases(self):
        self.cases = dict()
        with open('tests.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            k = 1
            for row in reader:
                data = ''.join(row).split(';')
                self.cases[k] = {'text': data[0], 'expected_tonal': data[1]}
                k += 1

