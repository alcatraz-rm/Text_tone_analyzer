# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import sqlite3
import os
import sys
sys.path.append(os.path.join('..', '..'))

from Python.Services.Logger import Logger

cwd = os.getcwd()


class DatabaseCursor:
    def __init__(self):
        # Services
        self.logger = Logger()

        if not self.logger.configured:
            self.logger.configure()

        # Data
        self.connection = None
        self.cursor = None

        self.logger.info('DatabaseCursor was successfully initialized.', 'DatabaseCursor.__init__()')

    def update_connection(self, ngram):
        if ngram.count(' ') == 0:

            if cwd.endswith('Master') or cwd.endswith('Temp') or cwd.endswith('Tests'):
                self.connection = sqlite3.connect(os.path.join('..', '..', 'Databases', 'unigrams.db'))

            elif cwd.endswith('Databases'):
                self.connection = sqlite3.connect('unigrams.db')

            self.cursor = self.connection.cursor()
            self.logger.info('Connected to database: unigrams.db', 'DatabaseCursor.UpdateConnection()')

        elif ngram.count(' ') == 1:

            if cwd.endswith('Master') or cwd.endswith('Temp') or cwd.endswith('Tests'):
                self.connection = sqlite3.connect(os.path.join('..', '..', 'Databases', 'bigrams.db'))

            elif cwd.endswith('Databases'):
                self.connection = sqlite3.connect('bigrams.db')

            self.cursor = self.connection.cursor()
            self.logger.info('Connected to database: bigrams.db', 'DatabaseCursor.UpdateConnection()')

        elif ngram.count(' ') == 2:

            if cwd.endswith('Master') or cwd.endswith('Temp') or cwd.endswith('Tests'):
                self.connection = sqlite3.connect(os.path.join('..', '..', 'Databases', 'trigrams.db'))

            elif cwd.endswith('Databases'):
                self.connection = sqlite3.connect('trigrams.db')

            self.cursor = self.connection.cursor()
            self.logger.info('Connected to database: trigrams.db', 'DatabaseCursor.UpdateConnection()')

    def get_info(self, ngram):
        self.update_connection(ngram)

        request = ("""
        SELECT * FROM 'Data' WHERE Ngram='%s'
        """) % ngram

        self.logger.info('request to DB: %s' % request, 'DatabaseCursor.get_info()')

        try:
            self.cursor.execute(request)
            self.logger.info('request is OK.', 'DatabaseCursor.get_info()')

        except sqlite3.DatabaseError or sqlite3.DataError:
            self.logger.error('DatabaseError', 'DatabaseCursor.get_info()')
            return None

        result = self.cursor.fetchone()
        self.logger.info('received data: %s' % str(result), 'DatabaseCursor.get_info()')

        if result:
            return result[1], result[2]
        else:
            return None, None

    def entry_exists(self, ngram):
        self.update_connection(ngram)

        request = ("""
        SELECT * FROM 'Data' WHERE Ngram='%s'
        """) % ngram

        self.logger.info('request to DB: %s' % request, 'DatabaseCursor.entry_exists()')

        try:
            self.cursor.execute(request)
            self.logger.info('request is OK.', 'DatabaseCursor.entry_exists()')

        except sqlite3.DatabaseError or sqlite3.DataError:
            self.logger.error('DatabaseError', 'DatabaseCursor.entry_exists()')
            return None

        if self.cursor.fetchone():
            self.logger.info('Entry exists: true', 'DatabaseCursor.entry_exists()')
            return True

        else:
            self.logger.info('Entry exists: false', 'DatabaseCursor.entry_exists()')
            return False
