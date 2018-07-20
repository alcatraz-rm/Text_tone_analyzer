# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


import csv
import json
import time
import unittest

import progressbar
from sklearn.metrics import classification_report

from Python.Master.TextTonalAnalyzer import Document


# vec_model = gensim.models.KeyedVectors.load_word2vec_format(os.path.join('..', 'databases',
#                                                                          'ruscorpora_upos_skipgram_300_10_2017.bin.gz'),
#                                                             binary=True)


class TonalTestCase(unittest.TestCase):
    def test(self):
        start_time = time.time()
        self.read_cases()
        self.test_results = {'Tests': list(), 'passed': 0, 'failed': 0, 'recall': None, 'F-measure': None,
                             'precision': None}

        with progressbar.ProgressBar(max_value=len(self.cases)) as bar:

            for case, data in self.cases.items():
                start_test_time = time.time()

                with self.subTest(case=case, test=data['text']):
                    doc = Document(data['text'])
                    doc.count_tonal()

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

                self.test_results['Tests'].append({'text': data['text'], 'case': case, 'result': doc.tonal, 'status': status,
                                                   'test runtime': end_test_time - start_test_time})

                bar.update(case)

        end_time = time.time()
        self.test_results['accuracy'] = round(self.test_results['passed'] / len(self.cases), 3) * 100
        self.test_results['total runtime'] = end_time - start_time
        self.metrics_count()

        with open('report_nbc_unigrams.json', 'w', encoding='utf-8') as file:
            json.dump(self.test_results, file, indent=4, ensure_ascii=False)

    def read_cases(self):
        # Change Dict to List
        self.cases = dict()
        with open('tests.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            k = 1

            for row in reader:
                data = ''.join(row).split(';')
                self.cases[k] = {'text': data[0], 'expected_tonal': data[1]}
                k += 1

    def metrics_count(self):
        y_true = list()
        y_pred = list()

        for test in self.test_results['Tests']:
            if test['status'] == 'passed':
                y_true.append(test['result'])
                y_pred.append(test['result'])

            elif test['result'] == 'positive':
                y_pred.append(test['result'])
                y_true.append('negative')

            else:
                y_pred.append(test['result'])
                y_true.append('positive')

        report = classification_report(y_true, y_pred, target_names=['negative', 'positive'],
                                       labels=['negative', 'positive'])

        metrics = report.split('\n')[5].split()
        self.test_results['precision'] = float(metrics[3])
        self.test_results['recall'] = float(metrics[4])
        self.test_results['F-measure'] = float(metrics[5])
