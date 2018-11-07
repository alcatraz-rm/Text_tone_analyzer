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

from flask import Flask, request

from Microservices import Packer
from Microservices.DocumentPreparer.DocumentPreparer import DocumentPreparer

server = Flask(__name__)
default_port = 5000

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


server.run(port=default_port)
