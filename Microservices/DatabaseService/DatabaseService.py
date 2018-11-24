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

import json
import os
import sqlite3

from Microservices import Packer, Logger
from flask import Flask, request

server = Flask(__name__)
logger = Logger.Logger()
default_port = 5003


class DatabaseCursor:
    def __init__(self):
        # Services
        # self._configurator = Configurator()
        # self._exceptions_handler = ExceptionsHandler()

        # Data
        self._wd = os.getcwd()
        self._request_url = None
        self._path_to_databases = DatabaseCursor._find_databases()
        self.databases_public_keys = None

        logger.info('DatabaseCursor was successfully initialized.', __name__)

    @staticmethod
    def _find_databases():
        wd = os.getcwd()

        # TODO: nesting level control

        while 'Data' not in os.listdir(os.getcwd()):
            os.chdir('..')

        path_to_databases = os.path.join(os.getcwd(), 'Data', 'Databases')

        os.chdir(wd)
        return path_to_databases

    def _load_config(self):
        path_to_config = os.path.join(self._path_to_databases, 'Configs', 'database_cursor.json')

        if os.path.exists(path_to_config):
            with open(path_to_config, 'r', encoding='utf-8') as file:
                config = json.load(file)

            self._request_url = config['request_url']
            self.databases_public_keys = config['database_public_keys']
        else:
            logger.error("Can't load config for DatabaseCursor (doesn't exist).", __name__)

    def __update_connection(self, ngram: str):
        path_to_db = None

        if ngram.count(' ') == 0:
            path_to_db = os.path.join(self._path_to_databases, 'unigrams.db')

        elif ngram.count(' ') == 1:
            path_to_db = os.path.join(self._path_to_databases, 'bigrams.db')

        elif ngram.count(' ') == 2:
            path_to_db = os.path.join(self._path_to_databases, 'trigrams.db')

        if path_to_db and os.path.exists(path_to_db):
            logger.info(f'Connected to database: {path_to_db}', __name__)

            return sqlite3.connect(path_to_db)

        # else:
        #     logger.warning(f'Database lost: {path_to_db}', __name__)
        #     logger.info('Trying to download database from cloud...', __name__)
        #
        #     # self._configurator.download_database(path_to_db)
        #
        #     self.__logger.info(f'Connected to database: {path_to_db}', __name__)

            # if os.path.exists(path_to_db):
            #     return sqlite3.connect(path_to_db)
            # else:
            #     self.__logger.fatal("Database doesn't exist.", __name__)

    def get_entry(self, ngram: str):
        connection = self.__update_connection(ngram)
        cursor = connection.cursor()

        requestDB = ("""
        SELECT * FROM 'Data' WHERE Ngram='%s'
        """) % ngram

        logger.info(f'Request to DB: {requestDB.strip()}', __name__)

        try:
            cursor.execute(requestDB)
            logger.info('Request is OK.', __name__)

        except BaseException as exception:
            connection.close()

            # logger.error(self._exceptions_handler.get_error_message(exception), __name__)
            return

        result = cursor.fetchone()
        logger.info(f'Received data: {str(result)}', __name__)

        if result:
            connection.close()

            return result[1], result[2]

        else:
            connection.close()

    def entry_exists(self, ngram: str):
        connection = self.__update_connection(ngram)
        cursor = connection.cursor()

        requestDB = ("""
        SELECT * FROM 'Data' WHERE Ngram='%s'
        """) % ngram

        logger.info(f'Request to DB: {requestDB.strip()}', __name__)

        try:
            cursor.execute(requestDB)
            logger.info('Request is OK.', __name__)

        except BaseException as exception:
            connection.close()

            # logger.error(self._exceptions_handler.get_error_message(exception), __name__)
            return

        if cursor.fetchone():
            connection.close()

            logger.info('Entry exists.', __name__)
            return True

        else:
            connection.close()

            logger.info("Entry doesn't exist.", __name__)
            return False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()

    def __del__(self):
        del self._request_url
        del self._wd


database_cursor = DatabaseCursor()


@server.route('/api/database/getData', methods=['GET'])
def get_data():
    logger.info(f'{request.method} request.', __name__)

    response = dict(response=dict(code=400))

    if 'content' in request.args:
        content = Packer.unpack(request.args['content'])
        logger.info(f'Params: {str(content)}', __name__)
    else:
        logger.error('Bad request.', __name__)
        return Packer.pack(response)

    if 'ngram' in content:
        ngram = content['ngram']

    else:
        return Packer.pack(response)

    with DatabaseCursor() as cursor:
        response['response']['pos_count'], response['response']['neg_count']\
            = cursor.get_entry(ngram)
        logger.info(f'Result: {str(response)}', __name__)

    response['response']['code'] = 200
    return Packer.pack(response)


@server.route('/api/database/entryExists', methods=['GEt'])
def entry_exist():
    logger.info(f'{request.method} request.', __name__)

    response = dict(response=dict(code=400))

    if 'content' in request.args:
        content = Packer.unpack(request.args['content'])
        logger.info(f'Params: {str(content)}', __name__)
    else:
        logger.error('Bad request.', __name__)
        return Packer.pack(response)

    if 'ngram' in content:
        ngram = content['ngram']
    else:
        return Packer.pack(response)

    with DatabaseCursor() as cursor:
        response['response']['entry_exist'] = cursor.entry_exists(ngram)

    logger.info(f'Result: {str(response)}', __name__)

    return Packer.pack(response)


try:
    server.run(port=default_port)
except BaseException as exception:
    logger.fatal(f'Error while trying to start server: {str(exception)}', __name__)

