# Copyright © 2017-2018. All rights reserved.
# Author: German Yakimov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su

import sqlite3
import os
from Python.Services.Logger import Logger

cwd = os.getcwd()


class DatabaseCursor:
    def __init__(self):
        # Services
        self.__logger = Logger()

        if not self.__logger.configured:
            self.__logger.configure()

        # Data
        self.__connection = None
        self.__cursor = None
        self.__current_db = None

        self.__logger.info('DatabaseCursor was successfully initialized.', 'DatabaseCursor.__init__()')

    def __update_connection(self, ngram):
        path_to_db = None

        if ngram.count(' ') == 0:

            if cwd.endswith('Python'):
                path_to_db = os.path.join('..', 'Databases', 'unigrams.db')

            elif cwd.endswith('Tests'):
                path_to_db = os.path.join('..', '..', 'Databases', 'unigrams.db')

            elif cwd.endswith('Databases'):
                path_to_db = 'unigrams.db'

        elif ngram.count(' ') == 1:

            if cwd.endswith('Python'):
                path_to_db = os.path.join('..', 'Databases', 'bigrams.db')

            elif cwd.endswith('Tests'):
                path_to_db = os.path.join('..', '..', 'Databases', 'bigrams.db')

            elif cwd.endswith('Databases'):
                path_to_db = 'bigrams.db'

        elif ngram.count(' ') == 2:

            if cwd.endswith('Python'):
                path_to_db = os.path.join('..', 'Databases', 'trigrams.db')

            elif cwd.endswith('Tests'):
                path_to_db = os.path.join('..', '..', 'Databases', 'trigrams.db')

            elif cwd.endswith('Databases'):
                path_to_db = 'trigrams.db'

        if os.path.exists(path_to_db) and path_to_db != self.__current_db:
            self.__connection = sqlite3.connect(path_to_db)
            self.__cursor = self.__connection.cursor()
            self.__current_db = path_to_db

            self.__logger.info('Connected to database: %s' % self.__current_db, 'DatabaseCursor.__update_connection()')

        elif not os.path.exists(path_to_db):
            self.__logger.fatal("Database doesn't exist.", 'DatabaseCursor.__update_connection()')

    def get_info(self, ngram):
        self.__update_connection(ngram)

        request = ("""
        SELECT * FROM 'Data' WHERE Ngram='%s'
        """) % ngram

        self.__logger.info('Request to DB: %s' % request.strip(), 'DatabaseCursor.get_info()')

        try:
            self.__cursor.execute(request)
            self.__logger.info('Request is OK.', 'DatabaseCursor.get_info()')

        except sqlite3.DatabaseError or sqlite3.DataError:
            self.__logger.error('DatabaseError.', 'DatabaseCursor.get_info()')
            return None

        result = self.__cursor.fetchone()
        self.__logger.info('Received data: %s' % str(result), 'DatabaseCursor.get_info()')

        if result:
            return result[1], result[2]
        else:
            return None, None

    def entry_exists(self, ngram):
        self.__update_connection(ngram)

        request = ("""
        SELECT * FROM 'Data' WHERE Ngram='%s'
        """) % ngram

        self.__logger.info('Request to DB: %s' % request.strip(), 'DatabaseCursor.entry_exists()')

        try:
            self.__cursor.execute(request)
            self.__logger.info('Request is OK.', 'DatabaseCursor.entry_exists()')

        except sqlite3.DatabaseError or sqlite3.DataError:
            self.__logger.error('DatabaseError.', 'DatabaseCursor.entry_exists()')
            return None

        if self.__cursor.fetchone():
            self.__logger.info('Entry exists: true.', 'DatabaseCursor.entry_exists()')
            return True

        else:
            self.__logger.info('Entry exists: false.', 'DatabaseCursor.entry_exists()')
            return False
