# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

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

        self.__logger.info('DatabaseCursor was successfully initialized.', 'DatabaseCursor.__init__()')

    def __update_connection(self, ngram):
        if ngram.count(' ') == 0:

            if cwd.endswith('Python') or cwd.endswith('Temp'):
                self.__connection = sqlite3.connect(os.path.join('..', 'Databases', 'unigrams.db'))

            elif cwd.endswith('Tests'):
                self.__connection = sqlite3.connect(os.path.join('..', '..', 'Databases', 'unigrams.db'))

            elif cwd.endswith('Databases'):
                self.__connection = sqlite3.connect('unigrams.db')

            self.__cursor = self.__connection.cursor()
            self.__logger.info('Connected to database: unigrams.db', 'DatabaseCursor.__update_connection()')

        elif ngram.count(' ') == 1:

            if cwd.endswith('Python') or cwd.endswith('Temp'):
                self.__connection = sqlite3.connect(os.path.join('..', 'Databases', 'bigrams.db'))

            elif cwd.endswith('Tests'):
                self.__connection = sqlite3.connect(os.path.join('..', '..', 'Databases', 'bigrams.db'))

            elif cwd.endswith('Databases'):
                self.__connection = sqlite3.connect('bigrams.db')

            self.__cursor = self.__connection.cursor()
            self.__logger.info('Connected to database: bigrams.db', 'DatabaseCursor.__update_connection(')

        elif ngram.count(' ') == 2:

            if cwd.endswith('Python') or cwd.endswith('Temp'):
                self.__connection = sqlite3.connect(os.path.join('..', 'Databases', 'trigrams.db'))

            elif cwd.endswith('Tests'):
                self.__connection = sqlite3.connect(os.path.join('..', '..', 'Databases', 'trigrams.db'))

            elif cwd.endswith('Databases'):
                self.__connection = sqlite3.connect('trigrams.db')

            self.__cursor = self.__connection.cursor()
            self.__logger.info('Connected to database: trigrams.db', 'DatabaseCursor.__update_connection(')

    def get_info(self, ngram):
        self.__update_connection(ngram)

        request = ("""
        SELECT * FROM 'Data' WHERE Ngram='%s'
        """) % ngram

        self.__logger.info('request to DB: %s' % request, 'DatabaseCursor.get_info()')

        try:
            self.__cursor.execute(request)
            self.__logger.info('request is OK.', 'DatabaseCursor.get_info()')

        except sqlite3.DatabaseError or sqlite3.DataError:
            self.__logger.error('DatabaseError', 'DatabaseCursor.get_info()')
            return None

        result = self.__cursor.fetchone()
        self.__logger.info('received data: %s' % str(result), 'DatabaseCursor.get_info()')

        if result:
            return result[1], result[2]
        else:
            return None, None

    def entry_exists(self, ngram):
        self.__update_connection(ngram)

        request = ("""
        SELECT * FROM 'Data' WHERE Ngram='%s'
        """) % ngram

        self.__logger.info('request to DB: %s' % request, 'DatabaseCursor.entry_exists()')

        try:
            self.__cursor.execute(request)
            self.__logger.info('request is OK.', 'DatabaseCursor.entry_exists()')

        except sqlite3.DatabaseError or sqlite3.DataError:
            self.__logger.error('DatabaseError', 'DatabaseCursor.entry_exists()')
            return None

        if self.__cursor.fetchone():
            self.__logger.info('Entry exists: true', 'DatabaseCursor.entry_exists()')
            return True

        else:
            self.__logger.info('Entry exists: false', 'DatabaseCursor.entry_exists()')
            return False
