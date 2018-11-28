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

import requests
from flask import Flask, request
import logging

from Microservices import Packer, Logger

server = Flask(__name__)
default_port = 5002
logger = Logger.Logger()


class SpellChecker:
    def __init__(self):
        # Services
        # self._exceptions_handler = ExceptionsHandler()

        logger.info('SpellChecker was successfully initialized.', __name__)

    def check_spelling(self, text: str):
        logger.info(f'Start text: {text}', __name__)

        try:
            response = requests.get('https://speller.yandex.net/services/spellservice.json/checkText', params={
                'text': text}).json()

        except BaseException as exception:
            # self.__logger.error(self._exceptions_handler.get_error_message(exception), __name__)
            return text

        for word in response:
            text = text.replace(word['word'], word['s'][0])

        logger.info(f'Checked text: {text}', __name__)
        return text


spell_checker = SpellChecker()


@server.route('/api/spellChecker/checkText', methods=['GET'])
def request_handle():
    logger.info(f'{request.method} request.', __name__)

    response = dict(response=dict(code=400))

    if 'content' in request.args:
        content = Packer.unpack(request.args['content'])
        logger.info(f'Params: {str(content)}', __name__)
    else:
        logger.error('Bad request.', __name__)
        return Packer.pack(response)

    if 'text' in content:
        text = content['text']
    else:
        return Packer.pack(response)

    response['response']['text'] = spell_checker.check_spelling(text)
    response['response']['code'] = 200

    return Packer.pack(response)


try:
    server.run(port=default_port)
    server.logger.setLevel(logging.CRITICAL)

except BaseException as exception:
    logger.fatal(f'Error while trying to start server: {str(exception)}', __name__)
