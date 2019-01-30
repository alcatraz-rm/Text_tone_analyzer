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


class ClassificationDataContainer:
    def __init__(self):
        self.classifiers = {'name': None,
                            'unigrams': None,
                            'bigrams': None,
                            'trigrams': None}

        self.tonalities = {'unigrams': None,
                           'bigrams': None,
                           'trigrams': None,
                           'final': None}

        self.weights = {'unigrams': None,
                        'bigrams': None,
                        'trigrams': None}

        self.probabilities = {'unigrams': 0,
                              'bigrams': 0,
                              'trigrams': 0,
                              'final': 0}

    def clear(self):
        self.classifiers = {item: None for item in self.classifiers}
        self.tonalities = {item: None for item in self.tonalities}
        self.tonalities['final'] = 'Unknown'
        self.weights = {item: None for item in self.weights}
        self.probabilities = {item: None for item in self.probabilities}
