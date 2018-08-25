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

import sqlite3
import os
import requests
from Python.Services.Logger import Logger
from Python.Services.PathService import PathService


class DatabaseCursor:
    def __init__(self):
        # Services
        self.__logger = Logger()

        if not self.__logger.configured:
            self.__logger.configure()

        self._path_service = PathService()

        # Data
        self._cwd = os.getcwd()
        self.__current_db = None

        # dump this information into config file

        self.databases_public_keys = {'unigrams.db': 'https://yadi.sk/d/tjOLg9oi3ZhYs4',
                                      'bigrams.db': 'https://yadi.sk/d/Ms4pkeV23ZhYrt',
                                      'trigrams.db': 'https://yadi.sk/d/J-B_zWpY3ZhYrz'}

        self.__logger.info('DatabaseCursor was successfully initialized.', 'DatabaseCursor.__init__()')

    def __update_connection(self, ngram):
        path_to_db = None

        if ngram.count(' ') == 0:
            path_to_db = self._path_service.get_path_to_database('unigrams.db')

        elif ngram.count(' ') == 1:
            path_to_db = self._path_service.get_path_to_database('bigrams.db')

        elif ngram.count(' ') == 2:
            path_to_db = self._path_service.get_path_to_database('trigrams.db')

        if path_to_db == self.__current_db:
            self.__logger.info('Connected to database: %s' % self.__current_db,
                               'DatabaseCursor.__update_connection()')

            return sqlite3.connect(path_to_db)

        elif os.path.exists(path_to_db):
            self.__current_db = path_to_db
            self.__logger.info('Connected to database: %s' % self.__current_db,
                               'DatabaseCursor.__update_connection()')

            return sqlite3.connect(path_to_db)

        elif not os.path.exists(path_to_db):
            self.__logger.warning('Database lost: %s' % path_to_db, 'DatabaseCursor.__update_connection()')

            try:
                self._download_database(path_to_db)

                self.__current_db = path_to_db

                self.__logger.info('Connected to database: %s' % self.__current_db,
                                   'DatabaseCursor.__update_connection()')

                return sqlite3.connect(path_to_db)

            except:
                self.__logger.fatal('Error when trying to download database from cloud.',
                                    'DatabaseCursor.__update_connection()')

                self.__logger.fatal("Database doesn't exist.", 'DatabaseCursor.__update_connection()')

    def _download_database(self, path_to_db):
        if self._cwd.endswith('Databases'):
            database_name = os.path.split(path_to_db)[0]
        else:
            database_name = os.path.split(path_to_db)[1]

        request_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download'

        download_url = requests.get(request_url, params={
            'public_key': self.databases_public_keys[database_name]
        }).json()["href"]

        response = requests.get(download_url)

        with open(path_to_db, 'wb') as database_file:
            database_file.write(response.content)

    def get_info(self, ngram):
        connection = self.__update_connection(ngram)
        cursor = connection.cursor()

        request = ("""
        SELECT * FROM 'Data' WHERE Ngram='%s'
        """) % ngram

        self.__logger.info('Request to DB: %s' % request.strip(), 'DatabaseCursor.get_info()')

        try:
            cursor.execute(request)
            self.__logger.info('Request is OK.', 'DatabaseCursor.get_info()')

        except sqlite3.DatabaseError or sqlite3.DataError:
            connection.close()

            self.__logger.error('DatabaseError.', 'DatabaseCursor.get_info()')
            return

        result = cursor.fetchone()
        self.__logger.info('Received data: %s' % str(result), 'DatabaseCursor.get_info()')

        if result:
            connection.close()

            return result[1], result[2]

        else:
            connection.close()

            return None, None

    def entry_exists(self, ngram):
        connection = self.__update_connection(ngram)
        cursor = connection.cursor()

        request = ("""
        SELECT * FROM 'Data' WHERE Ngram='%s'
        """) % ngram

        self.__logger.info('Request to DB: %s' % request.strip(), 'DatabaseCursor.entry_exists()')

        try:
            cursor.execute(request)
            self.__logger.info('Request is OK.', 'DatabaseCursor.entry_exists()')

        except sqlite3.DatabaseError or sqlite3.DataError:
            connection.close()

            self.__logger.error('DatabaseError.', 'DatabaseCursor.entry_exists()')
            return None

        except AttributeError:
            connection.close()

            self.__logger.error('AttributeError.', 'DatabaseCursor.entry_exists()')

        if cursor.fetchone():
            connection.close()

            self.__logger.info('Entry exists: true.', 'DatabaseCursor.entry_exists()')
            return True

        else:
            connection.close()

            self.__logger.info('Entry exists: false.', 'DatabaseCursor.entry_exists()')
            return False
