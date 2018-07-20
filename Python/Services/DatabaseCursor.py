# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


import sqlite3
import os

cwd = os.getcwd()


class DatabaseCursor:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def update_connection(self, ngram):
        if ngram.count(' ') == 0:
            if cwd.endswith('Master') or cwd.endswith('Temp') or cwd.endswith('Tests'):
                self.connection = sqlite3.connect(os.path.join('..', '..', 'Databases', 'unigrams.db'))
            elif cwd.endswith('Databases'):
                self.connection = sqlite3.connect('unigrams.db')

            self.cursor = self.connection.cursor()

        elif ngram.count(' ') == 1:
            if cwd.endswith('Master') or cwd.endswith('Temp') or cwd.endswith('Tests'):
                self.connection = sqlite3.connect(os.path.join('..', '..', 'Databases', 'bigrams.db'))
            elif cwd.endswith('Databases'):
                self.connection = sqlite3.connect('bigrams.db')

            self.cursor = self.connection.cursor()

        elif ngram.count(' ') == 2:
            if cwd.endswith('Master') or cwd.endswith('Temp') or cwd.endswith('Tests'):
                self.connection = sqlite3.connect(os.path.join('..', '..', 'Databases', 'trigrams.db'))
            elif cwd.endswith('Databases'):
                self.connection = sqlite3.connect('trigrams.db')

            self.cursor = self.connection.cursor()

    def get_info(self, ngram):
        self.update_connection(ngram)

        request = ("""
        SELECT * FROM 'Data' WHERE Ngram='%s'
        """) % ngram

        try:
            self.cursor.execute(request)
        except sqlite3.DatabaseError or sqlite3.DataError:
            return None

        result = self.cursor.fetchone()
        if result:
            return result[1], result[2]
        else:
            return None, None

    def entry_exists(self, ngram):
        self.update_connection(ngram)

        request = ("""
        SELECT * FROM 'Data' WHERE Ngram='%s'
        """) % ngram

        try:
            self.cursor.execute(request)
        except sqlite3.DatabaseError or sqlite3.DataError:
            return None

        if self.cursor.fetchone():
            return True
        else:
            return False
