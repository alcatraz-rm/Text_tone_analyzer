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
import requests
import os
import datetime
from Python.Services.Logger import Logger


class Configurator:
    def __init__(self):
        self.__logger = Logger()

        if not self.__logger.configured:
            self.__logger.configure()

        self._configuration = dict()
        self._cwd = os.getcwd()
        self._path_to_databases = None

        self.databases_public_keys = {'unigrams.db': 'https://yadi.sk/d/tjOLg9oi3ZhYs4',
                                      'bigrams.db': 'https://yadi.sk/d/Ms4pkeV23ZhYrt',
                                      'trigrams.db': 'https://yadi.sk/d/J-B_zWpY3ZhYrz'}

        # self.dataset_public_keys = {'dataset_with_unigrams.csv': 'https://yadi.sk/d/Goece_8r3Zk33G',
        #                             'dataset_with_bigrams.csv': 'https://yadi.sk/d/KQvjqfHF3Zk2xx',
        #                             'dataset_with_trigrams.csv': 'https://yadi.sk/d/zCoraYJ13Zk2zm'}

        self.__logger.info('Configurator was successfully initialized.', 'Configurator.__init__()')

    @staticmethod
    def _file_exists(filename):
        return os.path.exists(filename)

    def _download_database(self, path_to_db):
        database_name = os.path.split(path_to_db)[1]

        request_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download'

        download_url = requests.get(request_url, params={
            'public_key': self.databases_public_keys[database_name]
        }).json()["href"]

        response = requests.get(download_url)

        with open(path_to_db, 'wb') as database_file:
            database_file.write(response.content)

    @staticmethod
    def _download_vector_model(path_to_vector_model):
        request_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download'
        vector_model_url = 'https://yadi.sk/d/qoxAdYUC3ZcyrN'

        download_url = requests.get(request_url, params={
            'public_key': vector_model_url
        }).json()["href"]

        response = requests.get(download_url)

        with open(path_to_vector_model, 'wb') as vec_model:
            vec_model.write(response.content)

    def configure(self):
        databases_files = ['unigrams.db', 'bigrams.db', 'trigrams.db']

        self._configuration['datetime'] = str(datetime.datetime.now())

        while not os.getcwd().endswith('Python'):
            os.chdir('..')

        os.chdir(os.path.join('..', 'Databases'))
        self._path_to_databases = os.getcwd()
        os.chdir(self._cwd)

        for database in databases_files:
            path_to_database = os.path.join(self._path_to_databases, database)

            if not self._file_exists(path_to_database):
                try:
                    self._download_database(path_to_database)
                    self._configuration[database] = 'downloaded'
                except SystemError:
                    self._configuration[database] = 'error'
            else:
                self._configuration[database] = 'exists'

        path_to_vector_model = os.path.join(self._path_to_databases, 'ruscorpora_upos_skipgram_300_10_2017.bin.gz')

        if not os.path.exists(path_to_vector_model):
            try:
                self._download_vector_model(path_to_vector_model)
                self._configuration['ruscorpora_upos_skipgram_300_10_2017.bin.gz'] = 'downloaded'
            except SystemError:
                self._configuration['ruscorpora_upos_skipgram_300_10_2017.bin.gz'] = 'error'
        else:
            self._configuration['ruscorpora_upos_skipgram_300_10_2017.bin.gz'] = 'exists'

        self._create_config()

    def _create_config(self):
        with open(os.path.join('Logs', 'config.json'), 'w', encoding='utf-8') as config:
            json.dump(self._configuration, config, indent=4)
