import sqlite3
from datetime import datetime
import csv

conn = sqlite3.connect('words_database.db')
cursor = conn.cursor()
changes_date = str(datetime.now())


def check_word(word):
    with open('dictionary.txt', 'r', encoding='utf-8') as file:
        words_list = file.read().split('\n')
    if word in words_list:
        return True
    else:
        return False


def add_word_to_db(data):
    data = data.split(';')
    # if check_word(data[0]):
    request = ("""
    INSERT INTO [Words (Unfiltered)]
    VALUES ('%s', %d, %d, '%s')""" % (data[0], int(data[1]), int(data[2]), changes_date))
    cursor.execute(request)
    conn.commit()


def words_information_parse():
    with open('words_count.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        for num, row in enumerate(reader):
            add_word_to_db(''.join(row))
            print(str(num))


words_information_parse()
cursor.close()
