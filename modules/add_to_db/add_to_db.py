# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


from modules.lemmatization.lemmatization import lemmatization
from datetime import datetime
import csv


def add_docs_to_db():
    positive_docs_count = 0
    negative_docs_count = 0

    with open('positive_base.csv', 'a', encoding='utf-8') as pos_base:
        with open('positive-tmp.csv', 'r', encoding='utf-8') as file:
            positive_reader = csv.reader(file)
            try:
                for row in positive_reader:
                    row = lemmatization(''.join(row))
                    pos_base.write(row + '\n')
                    positive_docs_count += 1
            except:
                pass

    with open('negative_base.csv', 'a', encoding='utf-8') as neg_base:
        with open('negative-tmp.csv', 'r', encoding='utf-8') as file:
            negative_reader = csv.reader(file)
            try:
                for row in negative_reader:
                    row = lemmatization(''.join(row))
                    neg_base.write(row + '\n')
                    negative_docs_count += 1
            except:
                pass

    with open('docs_count.txt', 'w', encoding='utf-8') as file:
        file.write('%d\n' % (positive_docs_count))
        file.write('%d\n' % (negative_docs_count))
        file.write(str(datetime.now()))

    with open('positive-tmp.csv', 'w') as file:
        file.write('')

    with open('negative-tmp.csv', 'w') as file:
        file.write('')
