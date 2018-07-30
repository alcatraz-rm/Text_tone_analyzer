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
import json
import time
import unittest
from sklearn.metrics import classification_report
from Python.TextTonalAnalyzer import TextTonalAnalyzer


class TonalTestCase(unittest.TestCase):
    def test(self):
        text_tonal_analyzer = TextTonalAnalyzer()

        start_time = time.time()

        self.mode = 'fast-test'

        self.read_cases()
        self.test_results = {'Tests': list(), 'passed': 0, 'failed': 0, 'recall': None, 'F-measure': None,
                             'precision': None}

        for case, data in self.cases.items():
            print(case)
            start_test_time = time.time()

            with self.subTest(case=case, test=data['text']):
                text_tonal_analyzer.detect_tonal(data['text'])

                self.assertEqual(
                    data['expected_tonal'],
                    text_tonal_analyzer.tonal,
                )

            if text_tonal_analyzer.tonal == data['expected_tonal']:
                self.test_results['passed'] += 1
                status = 'passed'
            else:
                self.test_results['failed'] += 1
                status = 'failed'
            end_test_time = time.time()

            self.test_results['Tests'].append({'text': data['text'], 'case': case, 'result': text_tonal_analyzer.tonal,
                                               'status': status, 'test runtime': end_test_time - start_test_time})

        end_time = time.time()
        self.test_results['accuracy'] = round(self.test_results['passed'] / len(self.cases), 3)
        self.test_results['total runtime'] = end_time - start_time
        self.test_results['average runtime'] = self.test_results['total runtime'] / len(self.test_results['Tests'])
        self.metrics_count()

        with open('report_%s_%s.json' % (text_tonal_analyzer._classifier._classifier_name, self.mode),
                  'w', encoding='utf-8') as file:

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

                if self.mode == 'fast-test' and k == 50:
                    break

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
