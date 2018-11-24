import sys
import os
import subprocess
from flask import Flask, request, redirect
from Microservices import Packer, Logger
from urllib.parse import urlparse
import requests

server = Flask(__name__)
logger = Logger.Logger()
default_port = 5004


def get_services():
    wd = os.getcwd()

    services = [os.path.join(wd, 'DocumentPreparer', 'DocumentPreparer.py'),
                os.path.join(wd, 'DatabaseService', 'DatabaseService.py'),
                os.path.join(wd, 'Lemmatizer', 'Lemmatizer.py'),
                os.path.join(wd, 'SpellChecker', 'SpellChecker.py'),
                os.path.join(wd, 'FeatureExtractor', 'Extractor.py')]

    return services


def start_services():
    path_to_python = sys.executable

    services = get_services()

    for service in services:
        subprocess.Popen([path_to_python, service])
        print(f'{service} started.')


valid_methods = {
    'lemmatizer': {'getTextInitialForm': ['GET']},
    'database': {'entryExists': ['GET'],
                 'getData': ['GET']},
    'document': {'split_unigrams': ['GET'], 'split_bigrams': ['GET'], 'split_trigrams': ['GET']},
    'spellChecker': {'checkText': ['GET']},
    'featureExtraction': {'unigramsWeight': ['GET'], 'bigramsWeight': ['GET'],
                          'trigramsWeight': ['GET']}
                }

ports = {'lemmatizer': 5001, 'database': 5003, 'document': 5000,
         'spellChecker': 5002, 'featureExtraction': 5005}


@server.route('/api/<service>/<method>', methods=['GET'])
def handle_request(service, method):
    url = ['api']
    print(service, method)

    if service in valid_methods:
        # print(1)
        url.append(service)

        if method in valid_methods[service]:
            # print(2)
            url.append(method)

    if len(url) > 1:
        url = f'http://localhost:{ports[service]}/{"/".join(url)}'
    else:
        return Packer.pack(dict(response=dict(code=500)))

    # print(url)
    # print(dict(request.args))

    response = requests.get(url, params=dict(request.args)).content.decode('utf-8')
    # print(response)
    return response


start_services()

try:
    server.run(port=default_port)
except BaseException as exception:
    logger.fatal(f'Error while trying to start server: {str(exception)}', __name__)
