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

import re

from Python.Services.Logger import Logger


class DocumentPreparer:
    def __init__(self):
        self.__logger = Logger()

        self.__logger.info('DocumentPreparer was successfully initialized.', __name__)

    def split_into_unigrams(self, text: str):
        if text:
            return re.findall(r'\w+', text)
        else:
            self.__logger.warning('Got empty text.', __name__)

    def split_into_bigrams(self, text: str):
        if not text:
            self.__logger.warning('Got empty text.', __name__)
            return

        unigrams = self.split_into_unigrams(text)
        bigrams = list()

        if len(unigrams) >= 2:
            for unigram_index in range(len(unigrams) - 1):
                bigram = ' '.join(sorted([unigrams[unigram_index], unigrams[unigram_index + 1]])).strip()
                bigrams.append(bigram)

            return bigrams
        else:
            self.__logger.info("Text doesn't contain enough words.", __name__)

    def split_into_trigrams(self, text: str):
        if not text:
            self.__logger.warning('Got empty text.', __name__)
            return

        unigrams = self.split_into_unigrams(text)
        trigrams = list()

        if len(unigrams) >= 3:
            for unigram_index in range(len(unigrams) - 2):
                trigram = ' '.join(sorted(
                    [unigrams[unigram_index],
                     unigrams[unigram_index + 1],
                     unigrams[unigram_index + 2]])).strip()

                trigrams.append(trigram)

            return trigrams
        else:
            self.__logger.info("Text doesn't contain enough words.", __name__)

    def __del__(self):
        del self.__logger
