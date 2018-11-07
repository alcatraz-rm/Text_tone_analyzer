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


server.run(debug=True, port=default_port)
