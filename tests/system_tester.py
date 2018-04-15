# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


from modules.count_text_tonal.count_text_tonal import Document
from sklearn.metrics import classification_report
import csv
import time
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
        start_time = time.time()
        self.read_cases()
        self.test_results = {'tests': list(), 'passed': 0, 'failed': 0}

        for case, data in self.cases.items():
            start_test_time = time.time()
            with self.subTest(case=case, test=data['text']):
                doc = Document(data['text'], vec_model)
                doc.count_weight_by_unigrams()
                #doc.count_weight_by_bigrams()
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
            end_test_time = time.time()

            self.test_results['tests'].append({'text': data['text'], 'case': case, 'result': doc.tonal, 'status': status,
                                               'test runtime': end_test_time - start_test_time})

            print(case)

        end_time = time.time()
        self.test_results['accuracy'] = str(round(self.test_results['passed'] / len(self.cases), 3) * 100) + '%'
        self.test_results['total runtime'] = end_time - start_time

        with open('report_neg_200_ub.json', 'w', encoding='utf-8') as file:
            json.dump(self.test_results, file, indent=4, ensure_ascii=False)

    def read_cases(self):
        self.cases = dict()
        with open('10_tests_negative.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            k = 1
            for row in reader:
                data = ''.join(row).split(';')
                self.cases[k] = {'text': data[0], 'expected_tonal': data[1]}
                k += 1

    def tests_metrics(self):
        y_true = list()
        y_pred = list()
        for test in self.test_results['tests']:
            if test['status']== 'passed':
                y_true.append(test['result'])
                y_pred.append(test['result'])
            elif test['result'] == 'positive':
                y_pred.append(test['result'])
                y_true.append('negative')
            else:
                y_pred.append(test['result'])
                y_true.append('positive')
        report = classification_report(y_true, y_pred)
        metrics = report.split('\n')[6].split('       ')
        # self.metrics = {'precision': metrics[1], 'recall': metrics[2], 'F': metrics[3]}
        self.test_results['precision'] = metrics[1]
        self.test_results['recall'] = metrics[2]
        self.test_results['F'] = metrics[3]
