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

import json
import time
import unittest
from Python.Services.NgramAnalyzer import NgramAnalyzer

mode = 'unigrams'


class VecModelTest(unittest.TestCase):
    def test(self):
        ngram_analyzer = NgramAnalyzer()

        start_time = time.time()
        self.read_cases()
        self.test_results = {'Tests': list(), 'passed': 0, 'failed': 0}

        for n, case in enumerate(self.cases):
            print(n, case)
            start_test_time = time.time()

            with self.subTest(case=str(n) + case, test=case):
                relevant_ngram = ngram_analyzer.relevant_ngram_find(case)[0]

                if relevant_ngram:
                    self.test_results['passed'] += 1
                    status = 'passed'
                    self.assertEqual(True, True)

                else:
                    self.test_results['failed'] += 1
                    status = 'failed'
                    self.assertEqual(True, False)

            end_test_time = time.time()

            self.test_results['Tests'].append({'case': case, 'result': relevant_ngram,
                                               'status': status, 'test runtime': end_test_time - start_test_time})

        end_time = time.time()
        self.test_results['total runtime'] = end_time - start_time
        self.test_results['average runtime'] = self.test_results['total runtime'] / len(self.test_results['Tests'])

        with open('report_vector_model_%s.json' % mode, 'w', encoding='utf-8') as file:
            json.dump(self.test_results, file, indent=4, ensure_ascii=False)

    def read_cases(self):
        with open('unknown_%s.csv' % mode, 'r', encoding='utf-8') as file:
            self.cases = [case.strip() for case in file.readlines()]
