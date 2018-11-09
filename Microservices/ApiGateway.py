import sys
import os
import subprocess
from flask import Flask, request, redirect
from Microservices import Packer, Logger
from urllib.parse import urlparse

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
    'document': {'split': {'unigrams': ['GET'], 'bigrams': ['GET'], 'trigrams': ['GET']}},
    'spellChecker': {'checkText': ['GET']},
    'featureExtraction': {'unigramsWeight': ['GET'], 'bigramsWeight': ['GET'],
                          'trigramsWeight': ['GET']}
                }


@server.route('/api/<service>/<method>/<submethod>', methods=['GET'])
def handle_request(service, method, submethod):
    url = []

    if service in valid_methods:
        url.append(service)

        if method in valid_methods[service]:
            url.append(method)

            if submethod and submethod in valid_methods[service][method]:
                url.append(submethod)

    if url:
        url = '/'.join(url)

    response = redirect(url)
    return response


start_services()

try:
    server.run(port=default_port)
except BaseException as exception:
    logger.fatal(f'Error while trying to start server: {str(exception)}', __name__)
