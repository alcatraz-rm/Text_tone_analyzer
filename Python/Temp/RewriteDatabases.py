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

from Python.Services.PathService import PathService
import sqlite3

path_service = PathService()


def get_all_entries(database):
    path_to_db = path_service.get_path_to_database(database)

    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()

    request = "SELECT * FROM 'Data'"
    cursor.execute(request)

    return cursor.fetchall()


def optimize_data(data):
    return [[entry[0], entry[1], entry[2]] for entry in data]


def dump_to_csv(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for entry in data:
            entry[1], entry[2] = str(entry[1]), str(entry[2])
            file.write(';'.join(entry) + '\n')


# data = optimize_data(get_all_entries('trigrams.db'))
# dump_to_csv(data, 'trigrams_dump.csv')
