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
from Microservices.SpellChecker.SpellChecker import SpellChecker

server = Flask(__name__)
default_port = 5002

spell_checker = SpellChecker()


@server.route('/spellChecker/checkText', methods=['GET'])
def request_handle():
    response = dict(response=dict(code=400))

    if 'content' in request.args:
        content = Packer.unpack(request.args['content'])
    else:
        return Packer.pack(response)

    if 'text' in content:
        text = content['text']
    else:
        return Packer.pack(response)

    response['response']['text'] = spell_checker.check_spelling(text)
    response['response']['code'] = 200

    return Packer.pack(response)


server.run(port=default_port)
