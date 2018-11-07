import re


class DocumentPreparer:
    def __init__(self):
        pass
        # self.__logger = Logger()

        # self.__logger.info('DocumentPreparer was successfully initialized.', __name__)

    def split_into_unigrams(self, text: str):
        if text:
            return re.findall(r'\w+', text)
        # else:
        #     self.__logger.warning('Got empty text.', __name__)

    def split_into_bigrams(self, text: str):
        if not text:
            # self.__logger.warning('Got empty text.', __name__)
            return

        unigrams = self.split_into_unigrams(text)
        bigrams = list()

        if len(unigrams) >= 2:
            for unigram_index in range(len(unigrams) - 1):
                bigram = ' '.join(sorted([unigrams[unigram_index], unigrams[unigram_index + 1]])).strip()
                bigrams.append(bigram)

            return bigrams
        # else:
        # self.__logger.info("Text doesn't contain enough words.", __name__)

    def split_into_trigrams(self, text: str):
        if not text:
            # self.__logger.warning('Got empty text.', __name__)
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
        # else:
        #     self.__logger.info("Text doesn't contain enough words.", __name__)
