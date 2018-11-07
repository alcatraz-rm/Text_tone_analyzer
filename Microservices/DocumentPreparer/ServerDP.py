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
