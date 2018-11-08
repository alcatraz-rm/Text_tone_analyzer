import sys
import os
import subprocess
from flask import Flask, request
from Microservices import Packer, Logger

server = Flask(__name__)
logger = Logger.Logger()
default_port = 5004


def get_services():
    wd = os.getcwd()

    services = [os.path.join(wd, 'DocumentPreparer', 'DocumentPreparer.py'),
                os.path.join(wd, 'DatabaseService', 'DatabaseService.py'),
                os.path.join(wd, 'Lemmatizer', 'Lemmatizer.py'),
                os.path.join(wd, 'SpellChecker', 'SpellChecker.py')]
    return services


def start_services():
    path_to_python = sys.executable

    services = get_services()

    for service in services:
        subprocess.Popen([path_to_python, service])
        print(f'{service} started.')


start_services()

try:
    server.run(port=default_port)
except BaseException as exception:
    logger.fatal(f'Error while trying to start server: {str(exception)}', __name__)
