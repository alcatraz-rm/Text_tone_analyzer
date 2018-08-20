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

import os
import csv
import json
import time
import datetime
import unittest
import re
from sklearn.metrics import classification_report
from Python.TextTonalAnalyzer import TextTonalAnalyzer
from Python.Services.PathService import PathService


class TonalTestCase(unittest.TestCase):
    def _init(self):
        self._classifier_name = 'NBC'
        self._mode = 'full'

        self._text_tonal_analyzer = TextTonalAnalyzer(self._classifier_name)
        self._path_service = PathService()

        if not os.path.exists('Reports'):
            os.mkdir('Reports')

        self._test_results = {'Tests': list(), 'passed': 0, 'failed': 0, 'recall': None, 'F-measure': None,
                              'precision': None}

        self._cases = dict()
        self._read_cases()

    def test(self):
        self._init()

        sum_time = 0

        for case, data in self._cases.items():
            print(case)

            with self.subTest(case=case, test=data['text']):
                start_test_time = time.time()

                self._text_tonal_analyzer.detect_tonal(data['text'])

                end_test_time = time.time()

                self.assertEqual(
                    data['expected_tonal'],
                    self._text_tonal_analyzer.tonal,
                )

            if self._text_tonal_analyzer.tonal == data['expected_tonal']:
                self._test_results['passed'] += 1
                status = 'passed'
            else:
                self._test_results['failed'] += 1
                status = 'failed'

            test_time = end_test_time - start_test_time
            sum_time += test_time

            self._test_results['Tests'].append({'text': data['text'], 'case': case,
                                                'result': self._text_tonal_analyzer.tonal,
                                                'status': status, 'test runtime': test_time})

        self._record_results(sum_time)

        self._compare_results()

    def _record_results(self, sum_time):
        self._test_results['accuracy'] = round(self._test_results['passed'] / len(self._cases), 3)
        self._test_results['total runtime'] = sum_time
        self._test_results['average runtime'] = self._test_results['total runtime'] / len(self._test_results['Tests'])

        self._metrics_count()

        with open(os.path.join('Reports', 'report_%s_%s_%s.json' % (
                self._classifier_name,
                self._mode,
                str(datetime.datetime.now()).split('.')[0].replace(':', '-').replace(' ', '-'))),
                  'w', encoding='utf-8') as file:

            json.dump(self._test_results, file, indent=4, ensure_ascii=False)

    def _read_cases(self):
        with open('tests.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            k = 1

            for row in reader:
                data = ''.join(row).split(';')
                self._cases[k] = {'text': data[0], 'expected_tonal': data[1]}
                k += 1

                if self._mode == 'fast-test' and k == 51:
                    break

    def _metrics_count(self):
        y_true = list()
        y_pred = list()

        for test in self._test_results['Tests']:
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
        self._test_results['precision'] = float(metrics[3])
        self._test_results['recall'] = float(metrics[4])
        self._test_results['F-measure'] = float(metrics[5])

    @staticmethod
    def _convert_str_to_datetime(string):
        try:
            return datetime.datetime.strptime(string, '%Y-%m-%d-%H-%M-%S')
        except:
            pass

    def _last_report_find(self):
        path_to_reports = self._path_service.get_path_to_test_results('classifier')

        filenames = [filename for filename in os.listdir(path_to_reports)
                     if re.match(r'report_%s_%s_\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}.json' % (self._classifier_name,
                                                                                             self._mode), filename)]

        if len(filenames) < 2:
            return None

        files = dict()
        dt_objects = list()

        for filename in filenames:
            dt_object = self._convert_str_to_datetime(filename.split('_')[3].split('.')[0])

            if dt_object:
                files[dt_object] = filename
                dt_objects.append(dt_object)

        return os.path.join(path_to_reports, files[sorted(dt_objects)[len(dt_objects) - 2]])

    def _compare_results(self):
        compare_report = dict()

        last_report_path = self._last_report_find()

        if not last_report_path or not os.path.exists(last_report_path):
            return

        with open(last_report_path, 'r', encoding='utf-8') as file:
            last_report = json.load(file)

        compare_report['total runtime'] = self._test_results['total runtime'] - last_report['total runtime']
        compare_report['average runtime'] = self._test_results['average runtime'] - \
                                            last_report['average runtime']
        compare_report['failed'] = self._test_results['failed'] - last_report['failed']
        compare_report['passed'] = self._test_results['passed'] - last_report['passed']
        compare_report['recall'] = self._test_results['recall'] - last_report['recall']
        compare_report['accuracy'] = self._test_results['accuracy'] - last_report['accuracy']
        compare_report['precision'] = self._test_results['precision'] - last_report['precision']
        compare_report['F-measure'] = self._test_results['F-measure'] - last_report['F-measure']

        with open('compare_report.json', 'w', encoding='utf-8') as file:
            json.dump(compare_report, file, indent=4)
