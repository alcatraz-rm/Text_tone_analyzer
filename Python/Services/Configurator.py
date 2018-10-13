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

from datetime import datetime
import json
import os

import requests

from Python.Services.ExceptionsHandler import ExceptionsHandler
from Python.Services.Logger import Logger
from Python.Services.PathService import PathService
from Python.Services.Singleton import Singleton


class Configurator(metaclass=Singleton):
    def __init__(self):
        # Services
        self.__logger = Logger()
        self._path_service = PathService()
        self._exceptions_handler = ExceptionsHandler()

        # Data
        self._config = dict()
        self._wd = os.getcwd()
        self._path_to_databases = None
        self._request_url = None
        self._vector_model_public_key = None
        self._databases_public_keys = None

        self._load_public_keys()

        self.__logger.info('Configurator was successfully initialized.', __name__)

    def _load_public_keys(self):
        """
        Load public keys (links) from config-file (configurator.json) for downloading
        important files if it doesn't exist.

        Parameters: -
        Returns: -
        """
        path_to_config = os.path.join(self._path_service.path_to_configs, 'configurator.json')

        if os.path.exists(path_to_config):
            with open(path_to_config, 'r', encoding='utf-8') as file:
                config = json.load(file)

            self._request_url = config['request_url']
            self._vector_model_public_key = config['vector_model_public_key']
            self._databases_public_keys = config['databases_public_keys']

        else:
            self.__logger.error("Can't load config for Configrurator (doesn't exist).", __name__)

    def download_database(self, path_to_db):
        """
        Download database from Ya.Disk.

        Parameters:
            path_to_db: str
                Path to required database.
        Returns: -
        """

        database_name = os.path.split(path_to_db)[1]

        if database_name:
            try:
                download_url = requests.get(self._request_url, params={
                    'public_key': self._databases_public_keys[database_name]}).json()["href"]

                with open(path_to_db, 'wb') as database_file:
                    database_file.write(requests.get(download_url).content)

                self._config[path_to_db] = 'downloaded'

            except BaseException as exception:
                self.__logger.error(self._exceptions_handler.get_error_message(exception), __name__)
                self._config[path_to_db] = 'error'

    def download_vector_model(self):
        """
        Download vector model from Ya.Disk.

        Parameters: -
        Returns: -
        """

        self._path_service.set_path_to_vector_model(os.path.join(
            self._path_service.path_to_databases,
            'ruscorpora_upos_skipgram_300_10_2017.bin.gz'))

        try:
            download_url = requests.get(self._request_url, params={
                'public_key': self._vector_model_public_key}).json()["href"]

            with open(self._path_service.path_to_vector_model, 'wb') as vec_model:
                vec_model.write(requests.get(download_url).content)

            self._config['ruscorpora_upos_skipgram_300_10_2017.bin.gz'] = 'downloaded'

        except BaseException as exception:
            self.__logger.error(self._exceptions_handler.get_error_message(exception), __name__)

            self._config['ruscorpora_upos_skipgram_300_10_2017.bin.gz'] = 'error'

    def configure_system(self):
        """
        Configure system (check database and vector model existing,
        create config-file).

        Parameters: -
        Returns: -
        """

        self._config['datetime'] = str(datetime.now())

        for database in ['unigrams.db', 'bigrams.db', 'trigrams.db']:
            path_to_database = self._path_service.get_path_to_database(database)

            if not path_to_database or not os.path.exists(path_to_database):
                self.__logger.warning('Database not found: %s' % str(database), __name__)
                self.download_database(os.path.join(self._path_service.path_to_databases, database))
            else:
                self._config[database] = 'exists'

        if not self._path_service.path_to_vector_model or not os.path.exists(self._path_service.path_to_vector_model):
            self.__logger.warning('Vector model not found.', __name__)
            self.download_vector_model()
        else:
            self._config['ruscorpora_upos_skipgram_300_10_2017.bin.gz'] = 'exists'

        self._create_config()

    def _create_config(self):
        """
        Create config-file.

        Parameters: -
        Returns: -
        """

        with open(os.path.join('Logs', 'config.json'), 'w', encoding='utf-8') as config:
            json.dump(self._config, config, indent=4)
