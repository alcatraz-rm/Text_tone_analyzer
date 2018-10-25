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
import os

from Python.Services.Logger import Logger
from Python.Services.Singleton import Singleton


class PathService(metaclass=Singleton):
    def __init__(self):
        # Services
        self.__logger = Logger()

        # Data
        self._wd = os.getcwd()
        self.path_to_databases = None
        self.path_to_configs = None
        self._valid_classifiers = None
        self._valid_model_types = None
        self._valid_databases = None
        self._valid_test_results_modes = None
        self._valid_datasets = None
        self.path_to_stop_words = None
        self._path_to_main_directory = None
        self.path_to_vector_model = None
        self._path_to_classifier_models = None
        self._path_to_test_results = None
        self.path_to_vectorizer = None

        self.configure()
        self.__logger.info('PathService was successfully configured.', __name__)

    def _find_main_directory(self):
        max_nesting_level = 5
        nesting_level = 0

        while not os.getcwd().endswith('Python'):
            if os.getcwd().endswith('Databases'):
                os.chdir(os.path.join('..', 'Python'))
                break
            else:
                os.chdir('..')

            nesting_level += 1

            if nesting_level > max_nesting_level:
                self.__logger.fatal("Can't find main directory (exceeded maximum nesting level).", __name__)
                exit(-1)

        self._path_to_main_directory = os.getcwd()
        self.path_to_configs = os.path.join(self._path_to_main_directory, 'Services', 'Configs')
        self.path_to_databases = os.path.abspath(os.path.join('..', 'Databases'))

        os.chdir(self._wd)

    def _check_paths_existing(self):
        if not os.path.exists(self.path_to_configs):
            self.__logger.fatal("Directory with config files doesn't exist.", __name__)
            exit(-1)

        elif not os.path.exists(self.path_to_databases):
            self.__logger.fatal("Directory with databases doesn't exist.", __name__)
            exit(-1)

        elif not os.path.exists(self._path_to_classifier_models):
            self.__logger.fatal("Directory with classifier models doesn't exist.", __name__)
            exit(-1)

        if not os.path.exists(self.path_to_vector_model):
            self.path_to_vector_model = None
            self.__logger.error("Vector model doesn't exist.", __name__)

        if not os.path.exists(self.path_to_stop_words):
            self.path_to_stop_words = None
            self.__logger.error("File with stop-words doesn't exist.", __name__)

        if not os.path.exists(self.path_to_vectorizer):
            self.path_to_vectorizer = None
            self.__logger.error("Vectorizer model not found.", __name__)

        if not os.path.exists(self._path_to_test_results):
            self._path_to_test_results = None
            self.__logger.warning("Directory with tests reports doesn't exist.", __name__)

    def _load_config(self):
        path_to_config = os.path.join(self.path_to_configs, 'path_service.json')

        if not os.path.exists(path_to_config):
            self.__logger.error("Can't find config-file for PathService.", __name__)

        with open(path_to_config, 'r', encoding='utf-8') as file:
            config = json.load(file)

        self._valid_classifiers = config['valid_classifiers']
        self._valid_databases = config['valid_databases']
        self._valid_datasets = config['valid_datasets']
        self._valid_test_results_modes = config['valid_test_results_modes']
        self._valid_model_types = config['valid_model_types']

    def configure(self):
        self._find_main_directory()
        self._load_config()

        self.path_to_vector_model = os.path.join(self.path_to_databases, 'ruscorpora_upos_skipgram_300_10_2017.bin.gz')
        self.path_to_stop_words = os.path.join(self._path_to_main_directory, 'Services', 'Lemmatizer',
                                               'stop_words.json')
        self._path_to_classifier_models = os.path.join(self.path_to_databases, 'Models')
        self._path_to_test_results = os.path.join(self._path_to_main_directory, 'Tests', 'System', 'Reports')

        self.path_to_vectorizer = os.path.join(self.path_to_databases, 'vectorizer.pkl')

        self._check_paths_existing()

    def get_path_to_test_results(self, mode='classifier', classifier_name='NBC'):
        if classifier_name not in self._valid_classifiers:
            self.__logger.warning('Got incorrect classifier name.', __name__)
            classifier_name = 'NBC'

        if classifier_name not in self._valid_test_results_modes:
            self.__logger.warning('Got incorrect mode.', __name__)
            return self._path_to_test_results

        if mode.lower().strip() == 'vec_model':
            return os.path.join(self._path_to_test_results, 'VectorModel')

        elif mode.lower().strip() == 'classifier_main':
            return os.path.join(self._path_to_test_results, '..', '..', 'MainReports', 'Classifier', classifier_name)

        elif mode.lower().strip() == 'classifier':
            return self._path_to_test_results

    def get_path_to_model(self, model='unigrams', classifier_name='NBC'):
        if classifier_name not in self._valid_classifiers:
            self.__logger.warning('Got incorrect classifier name.', __name__)
            classifier_name = 'NBC'

        if model not in self._valid_model_types:
            self.__logger.warning('Got incorrect model type.', __name__)
            model = 'unigrams'

        path_to_models = os.path.join(self._path_to_classifier_models, classifier_name)

        if os.path.exists(path_to_models):
            path_to_required_model = os.path.join(path_to_models, f'model_{model}.pkl')

            return path_to_required_model
        else:
            self.__logger.error("Required model wasn't found.", __name__)

    def get_path_to_database(self, database_name='unigrams.db'):
        if database_name not in self._valid_databases:
            self.__logger.warning('Got incorrect database name.', __name__)
            database_name = 'unigrams.db'

        path_to_database = os.path.join(self.path_to_databases, database_name)

        return path_to_database

    def get_path_to_dataset(self, dataset):
        if dataset not in self._valid_datasets:
            self.__logger.warning('Got incorrect dataset name.', __name__)
            dataset = 'dataset_with_unigrams.csv'

        path_to_dataset = os.path.join(self.path_to_databases, dataset)

        return path_to_dataset

    def set_path_to_vector_model(self, path_to_vector_model):
        self.path_to_vector_model = path_to_vector_model
