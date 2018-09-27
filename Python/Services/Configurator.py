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

        self._config = dict()
        self._wd = os.getcwd()
        self._path_to_databases = None
        self._request_url = None
        self._vector_model_public_key = None
        self._databases_public_keys = None

        self.__logger.info('Configurator was successfully initialized.', 'Configurator.__init__()')

    def _load_links(self):
        with open(os.path.join(self._path_service.path_to_configs, 'configurator.json'),
                  'r', encoding='utf-8') as file:
            config = json.load(file)

        self._request_url = config['request_url']
        self._vector_model_public_key = config['vector_model_public_key']
        self._databases_public_keys = config['databases_public_keys']

    def _download_database(self, path_to_db):
        database_name = os.path.split(path_to_db)[1]

        download_url = requests.get(self._request_url, params={
            'public_key': self._databases_public_keys[database_name]}).json()["href"]

        with open(path_to_db, 'wb') as database_file:
            database_file.write(requests.get(download_url).content)

    def download_vector_model(self):
        self._path_service.set_path_to_vector_model(os.path.join(
            self._path_service.path_to_databases,
            'ruscorpora_upos_skipgram_300_10_2017.bin.gz'))

        download_url = requests.get(self._request_url, params={
            'public_key': self._vector_model_public_key}).json()["href"]

        with open(self._path_service.path_to_vector_model, 'wb') as vec_model:
            vec_model.write(requests.get(download_url).content)

    def configure(self):
        self._config['datetime'] = str(datetime.datetime.now())

        for database in ['unigrams.db', 'bigrams.db', 'trigrams.db']:
            path_to_database = self._path_service.get_path_to_database(database)

            if not os.path.exists(path_to_database):
                try:
                    self._download_database(path_to_database)
                    self._config[database] = 'downloaded'
                except:
                    self._config[database] = 'error'
            else:
                self._config[database] = 'exists'

        if not self._path_service.path_to_vector_model:
            try:
                self.download_vector_model()
                self._config['ruscorpora_upos_skipgram_300_10_2017.bin.gz'] = 'downloaded'
            except:
                self._config['ruscorpora_upos_skipgram_300_10_2017.bin.gz'] = 'error'
        else:
            self._config['ruscorpora_upos_skipgram_300_10_2017.bin.gz'] = 'exists'
            return

        self._create_config()

    def _create_config(self):
        with open(os.path.join('Logs', 'config.json'), 'w', encoding='utf-8') as config:
            json.dump(self._config, config, indent=4)
