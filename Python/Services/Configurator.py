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
from Python.Services.PathService import PathService


class Configurator:
    def __init__(self):
        self.__logger = Logger()

        if not self.__logger.configured:
            self.__logger.configure()

        self._path_service = PathService()

        self._configuration = dict()
        self._cwd = os.getcwd()
        self._path_to_databases = None

        self.databases_public_keys = {'unigrams.db': 'https://yadi.sk/d/tjOLg9oi3ZhYs4',
                                      'bigrams.db': 'https://yadi.sk/d/Ms4pkeV23ZhYrt',
                                      'trigrams.db': 'https://yadi.sk/d/J-B_zWpY3ZhYrz'}

        self.__logger.info('Configurator was successfully initialized.', 'Configurator.__init__()')

    def _download_database(self, path_to_db):
        database_name = os.path.split(path_to_db)[1]

        request_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download'

        download_url = requests.get(request_url, params={
            'public_key': self.databases_public_keys[database_name]
        }).json()["href"]

        response = requests.get(download_url)

        with open(path_to_db, 'wb') as database_file:
            database_file.write(response.content)

    def _download_vector_model(self):
        if not self._path_service.path_to_vector_model:
            self._configuration['ruscorpora_upos_skipgram_300_10_2017.bin.gz'] = 'downloaded'

            self._path_service.set_path_to_vector_model(os.path.join(
                self._path_service.path_to_databases,
                'ruscorpora_upos_skipgram_300_10_2017.bin.gz'
            ))
        else:
            self._configuration['ruscorpora_upos_skipgram_300_10_2017.bin.gz'] = 'exists'
            return

        request_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download'
        vector_model_url = 'https://yadi.sk/d/qoxAdYUC3ZcyrN'

        download_url = requests.get(request_url, params={
            'public_key': vector_model_url
        }).json()["href"]

        response = requests.get(download_url)

        with open(self._path_service.path_to_vector_model, 'wb') as vec_model:
            vec_model.write(response.content)

    def configure(self):
        databases_files = ['unigrams.db', 'bigrams.db', 'trigrams.db']

        self._configuration['datetime'] = str(datetime.datetime.now())

        for database in databases_files:
            path_to_database = self._path_service.get_path_to_database(database)

            if not path_to_database:
                try:
                    self._download_database(path_to_database)
                    self._configuration[database] = 'downloaded'
                except:
                    self._configuration[database] = 'error'
            else:
                self._configuration[database] = 'exists'

        try:
            self._download_vector_model()
        except:
            pass

        self._create_config()

    def _create_config(self):
        with open(os.path.join('Logs', 'config.json'), 'w', encoding='utf-8') as config:
            json.dump(self._configuration, config, indent=4)
