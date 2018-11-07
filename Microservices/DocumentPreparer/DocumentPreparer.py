from flask import Flask, request
from Microservices import Packer
import re
import json


server = Flask(__name__)


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


document_preparer = DocumentPreparer()


@server.route('/document/split/unigrams', methods=['GET'])
def handle_u():
    response = dict(response=dict(code=400))

    if 'content' in request.args:
        args = Packer.unpack(request.args['content'])
    else:
        return Packer.pack(response)

    if 'text' in args:
        text = args['text']
    else:
        return Packer.pack(response)

    response['response']['unigrams'] = document_preparer.split_into_unigrams(text)
    response['response']['code'] = 200

    return Packer.pack(response)


@server.route('/document/split/bigrams', methods=['GET'])
def handle_b():
    response = dict(response=dict(code=400))

    if 'content' in request.args:
        args = Packer.unpack(request.args['content'])
    else:
        return Packer.pack(response)

    if 'text' in args:
        text = args['text']
    else:
        return Packer.pack(response)

    response['response']['bigrams'] = document_preparer.split_into_bigrams(text)
    response['response']['code'] = 200

    return Packer.pack(response)


@server.route('/document/split/trigrams', methods=['GET'])
def handle_t():
    response = dict(response=dict(code=400))

    if 'content' in request.args:
        args = Packer.unpack(request.args['content'])
    else:
        return Packer.pack(response)

    if 'text' in args:
        text = args['text']
    else:
        return Packer.pack(response)

    response['response']['trigrams'] = document_preparer.split_into_trigrams(text)
    response['response']['code'] = 200

    return Packer.pack(response)


server.run(debug=True)
