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

from flask import Flask, request

from Microservices import Packer, Logger

server = Flask(__name__)
logger = Logger.Logger()
default_port = 5000


class DocumentPreparer:
    def __init__(self):
        logger.info('DocumentPreparer was successfully initialized.', __name__)

    def split_into_unigrams(self, text: str):
        if text:
            return re.findall(r'\w+', text)
        else:
            logger.warning('Got empty text.', __name__)

    def split_into_bigrams(self, text: str):
        if not text:
            logger.warning('Got empty text.', __name__)
            return

        unigrams = self.split_into_unigrams(text)
        bigrams = list()

        if len(unigrams) >= 2:
            for unigram_index in range(len(unigrams) - 1):
                bigram = ' '.join(sorted([unigrams[unigram_index], unigrams[unigram_index + 1]])).strip()
                bigrams.append(bigram)

            return bigrams
        else:
            logger.info("Text doesn't contain enough words.", __name__)

    def split_into_trigrams(self, text: str):
        if not text:
            logger.warning('Got empty text.', __name__)
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
            logger.info("Text doesn't contain enough words.", __name__)


document_preparer = DocumentPreparer()


@server.route('/document/split/unigrams', methods=['GET'])
def handle_u():
    logger.info(f'{request.method} request.', __name__)

    response = dict(response=dict(code=400))

    if 'content' in request.args:
        args = Packer.unpack(request.args['content'])
        logger.info(f'Params: {str(args)}', __name__)

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
    logger.info(f'{request.method} request.', __name__)

    response = dict(response=dict(code=400))

    if 'content' in request.args:
        args = Packer.unpack(request.args['content'])
    else:
        return Packer.pack(response)

    if 'text' in args:
        text = args['text']
        logger.info(f'Params: {str(args)}', __name__)

    else:
        return Packer.pack(response)

    response['response']['bigrams'] = document_preparer.split_into_bigrams(text)
    response['response']['code'] = 200

    return Packer.pack(response)


@server.route('/document/split/trigrams', methods=['GET'])
def handle_t():
    logger.info(f'{request.method} request.', __name__)

    response = dict(response=dict(code=400))

    if 'content' in request.args:
        args = Packer.unpack(request.args['content'])
        logger.info(f'Params: {str(args)}', __name__)

    else:
        return Packer.pack(response)

    if 'text' in args:
        text = args['text']
    else:
        return Packer.pack(response)

    response['response']['trigrams'] = document_preparer.split_into_trigrams(text)
    response['response']['code'] = 200

    return Packer.pack(response)


try:
    server.run(port=default_port)
except BaseException as exception:
    logger.fatal(f'Error while trying to start server: {str(exception)}', __name__)
