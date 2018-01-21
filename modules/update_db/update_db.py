# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


import sqlite3
from datetime import datetime
import csv
from modules.lemmatization.lemmatization import lemmatization


conn = sqlite3.connect('words_database.db')
cursor = conn.cursor()
changes_date = str(datetime.now())


def tmp_docs_lemmatization():
    with open('positive-tmp.csv', 'r', encoding='utf-8') as pos_tmp:
        with open('positive-tmp-lemmatization.csv', 'w', encoding='utf-8') as pos_tmp_lemm:
            pos_tmp_reader = csv.reader(pos_tmp)
            print('Starting positive docs lemmatization...')
            try:
                for num, row in enumerate(pos_tmp_reader):
                    print(num)
                    row = lemmatization(''.join(row))
                    pos_tmp_lemm.write(row + '\n')
            except:
                pass

    with open('negative-tmp.csv', 'r', encoding='utf-8') as neg_tmp:
        with open('negative-tmp-lemmatization.csv', 'w', encoding='utf-8') as neg_tmp_lemm:
            neg_tmp_reader = csv.reader(neg_tmp)
            print('Starting negative docs lemmatization...')
            try:
                for num, row in enumerate(neg_tmp_reader):
                    print(num)
                    row = lemmatization(''.join(row))
                    neg_tmp_lemm.write(row + '\n')
            except:
                pass


def update_db():
    tmp_docs_lemmatization()
