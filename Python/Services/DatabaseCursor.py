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

from Python.Services.Configurator import Configurator
from Python.Services.ExceptionsHandler import ExceptionsHandler
from Python.Services.Logger import Logger
from Python.Services.PathService import PathService


class DatabaseCursor:
    def __init__(self):
        # Services
        self.__logger = Logger()
        self._path_service = PathService()
        self._configurator = Configurator()
        self._exceptions_handler = ExceptionsHandler()

        # Data
        self._wd = os.getcwd()
        self._request_url = None
        self.databases_public_keys = None

        self.__logger.info('DatabaseCursor was successfully initialized.', __name__)

    def _load_config(self):
        path_to_config = os.path.join(self._path_service.path_to_configs, 'database_cursor.json')

        if os.path.exists(path_to_config):
            with open(path_to_config, 'r', encoding='utf-8') as file:
                config = json.load(file)

            self._request_url = config['request_url']
            self.databases_public_keys = config['database_public_keys']
        else:
            self.__logger.error("Can't load config for DatabaseCursor (doesn't exist).", __name__)

    def __update_connection(self, ngram: str):
        path_to_db = None

        if ngram.count(' ') == 0:
            path_to_db = self._path_service.get_path_to_database('unigrams.db')

        elif ngram.count(' ') == 1:
            path_to_db = self._path_service.get_path_to_database('bigrams.db')

        elif ngram.count(' ') == 2:
            path_to_db = self._path_service.get_path_to_database('trigrams.db')

        if path_to_db and os.path.exists(path_to_db):
            self.__logger.info(f'Connected to database: {path_to_db}', __name__)

            return sqlite3.connect(path_to_db)

        else:
            self.__logger.warning(f'Database lost: {path_to_db}', __name__)
            self.__logger.info('Trying to download database from cloud...', __name__)

            self._configurator.download_database(path_to_db)

            self.__logger.info(f'Connected to database: {path_to_db}', __name__)

            if os.path.exists(path_to_db):
                return sqlite3.connect(path_to_db)
            else:
                self.__logger.fatal("Database doesn't exist.", __name__)

    def get_entry(self, ngram: str):
        connection = self.__update_connection(ngram)
        cursor = connection.cursor()

        request = ("""
        SELECT * FROM 'Data' WHERE Ngram='%s'
        """) % ngram

        self.__logger.info(f'Request to DB: {request.strip()}', __name__)

        try:
            cursor.execute(request)
            self.__logger.info('Request is OK.', __name__)

        except BaseException as exception:
            connection.close()

            self.__logger.error(self._exceptions_handler.get_error_message(exception), __name__)
            return

        result = cursor.fetchone()
        self.__logger.info(f'Received data: {str(result)}', __name__)

        if result:
            connection.close()

            return result[1], result[2]

        else:
            connection.close()

    def entry_exists(self, ngram: str):
        connection = self.__update_connection(ngram)
        cursor = connection.cursor()

        request = ("""
        SELECT * FROM 'Data' WHERE Ngram='%s'
        """) % ngram

        self.__logger.info(f'Request to DB: {request.strip()}', __name__)

        try:
            cursor.execute(request)
            self.__logger.info('Request is OK.', __name__)

        except BaseException as exception:
            connection.close()

            self.__logger.error(self._exceptions_handler.get_error_message(exception), __name__)
            return

        if cursor.fetchone():
            connection.close()

            self.__logger.info('Entry exists.', __name__)
            return True

        else:
            connection.close()

            self.__logger.info("Entry doesn't exist.", __name__)
            return False
