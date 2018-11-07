from flask import Flask, request

from Microservices import Packer
from Microservices.Lemmatizer.Lemmatizer import Lemmatizer

server = Flask(__name__)
default_port = 5001

lemmatizer = Lemmatizer()


@server.route('/lemmatizer/getTextInitialForm', methods=['GET'])
def handle():
    response = dict(response=dict(code=400))

    if 'content' in request.args:
        content = Packer.unpack(request.args['content'])
    else:
        return Packer.pack(response)

    if 'text' in content:
        text = content['text']
    else:
        return Packer.pack(response)

    response['response']['lemmatized_text'] = lemmatizer.get_text_initial_form(text)

    return Packer.pack(response)


server.run(debug=True, port=default_port)
