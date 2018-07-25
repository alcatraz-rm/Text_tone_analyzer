# Copyright © 2018. All rights reserved.
# Author: German Yakimov
# Licensed under the Apache License, Version 2.0
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE

from Python.Services.Logger import Logger


class DocumentPreparer:
    def __init__(self):
        self.__logger = Logger()

        if not self.__logger.configured:
            self.__logger.configure()

        self.__logger.info('DocumentPreparer was successfully initialized.', 'DocumentPreparer.__init__()')

    @staticmethod
    def split_into_unigrams(text):
        return text.split()

    @staticmethod
    def split_into_bigrams(text):
        unigrams = text.split()
        bigrams = list()

        if len(unigrams) >= 2:
            for unigram_index in range(len(unigrams) - 1):
                bigrams.append(unigrams[unigram_index] + ' ' + unigrams[unigram_index + 1])

            return bigrams

    @staticmethod
    def split_into_trigrams(text):
        unigrams = text.split()
        trigrams = list()

        if len(unigrams) >= 3:
            for unigram_index in range(len(unigrams) - 2):
                trigrams.append(unigrams[unigram_index] + ' ' + unigrams[unigram_index + 1] + ' ' +
                                unigrams[unigram_index + 2])

            return trigrams
