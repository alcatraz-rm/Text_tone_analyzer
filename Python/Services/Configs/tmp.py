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


data = {'possible_classifiers': ['NBC', 'LogisticRegression', 'KNN'],
        'possible_model_types': ['unigrams', 'bigrams', 'trigrams'],
        'possible_databases': ['unigrams.db', 'bigrams.db', 'trigrams.db'],
        'possible_test_results_modes': ['classifier', 'classifier_main', 'vec_model'],
        'possible_datasets': ['dataset_with_unigrams.csv', 'dataset_with_bigrams.csv',
                              'dataset_with_trigrams.csv']}

with open('path_service.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4)
