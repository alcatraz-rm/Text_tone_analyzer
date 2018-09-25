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


class ClassifierDataContainer:
    def __init__(self):
        self.classifier_name = None
        self.unigrams_classifier = None
        self.bigrams_classifier = None
        self.trigrams_classifier = None

        self.unigrams_tonal = None
        self.bigrams_tonal = None
        self.trigrams_tonal = None

        self.unigrams_weight = None
        self.bigrams_weight = None
        self.trigrams_weight = None

        self.unigrams_probability = 0
        self.bigrams_probability = 0
        self.trigrams_probability = 0

        self.tonal = None
        self.probability = 0

    def reset(self):
        self.classifier_name = None
        self.unigrams_classifier = None
        self.bigrams_classifier = None
        self.trigrams_classifier = None

        self.unigrams_tonal = None
        self.bigrams_tonal = None
        self.trigrams_tonal = None

        self.unigrams_weight = None
        self.bigrams_weight = None
        self.trigrams_weight = None

        self.unigrams_probability = 0
        self.bigrams_probability = 0
        self.trigrams_probability = 0

        self.tonal = None
        self.probability = 0
