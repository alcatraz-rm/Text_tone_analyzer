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

import os
from Python.Services.Logger import Logger
from Python.Services.Singleton.Singleton import Singleton


class PathService(metaclass=Singleton):
    def __init__(self):
        self.__logger = Logger()

        if not self.__logger.configured:
            self.__logger.configure()

        self._cwd = os.getcwd()
        self.path_to_databases = None

        # dump this information in config file

        self._possible_classifiers = ['NBC', 'LogisticRegression', 'KNN']
        self._possible_model_types = ['unigrams', 'bigrams', 'trigrams']
        self._possible_databases = ['unigrams.db', 'bigrams.db', 'trigrams.db']
        self._possible_test_results_modes = ['classifier', 'classifier_main', 'vec_model']
        self._possible_datasets = ['dataset_with_unigrams.csv', 'dataset_with_bigrams.csv',
                                   'dataset_with_trigrams.csv']

        self.path_to_parts_of_speech = None
        self._path_to_main_directory = None

        self.path_to_vector_model = None
        self._path_to_classifier_models = None

        self._path_to_test_results = None

        self.configure()
        self.__logger.info('PathService was successfully configured.', 'PathService.__init__()')

    def _find_main_directory(self):
        counter = 0

        while not os.getcwd().endswith('Python'):
            os.chdir('..')

            if os.getcwd().endswith('Databases'):
                os.chdir('..')
                break

            counter += 1

            if counter > 5:
                self.__logger.fatal("Can't find main directory.", 'PathService._find_main_directory()')
                return

        self._path_to_main_directory = os.getcwd()

        self.path_to_databases = os.path.abspath(os.path.join('..', 'Databases'))
        os.chdir(self._cwd)

    def configure(self):
        self._find_main_directory()

        self.path_to_vector_model = os.path.join(self.path_to_databases, 'ruscorpora_upos_skipgram_300_10_2017.bin.gz')

        if not os.path.exists(self.path_to_vector_model):
            self.__logger.info("Vector model wasn't found.", 'PathService.configure()')
            self.path_to_vector_model = None

        self.path_to_parts_of_speech = os.path.join(self._path_to_main_directory, 'Services',
                                                    'Lemmatizer', 'parts_of_speech.json')

        if not os.path.exists(self.path_to_parts_of_speech):
            self.__logger.warning("File with parts of speech wasn't found.", 'PathService.configure()')
            self.path_to_parts_of_speech = None

        self._path_to_classifier_models = os.path.join(self.path_to_databases, 'Models')

        if not os.path.exists(self._path_to_classifier_models):
            self.__logger.error("Classifier models wasn't found.", 'PathService.configure()')
            self._path_to_classifier_models = None

        self._path_to_test_results = os.path.join(self._path_to_main_directory, 'Tests', 'System', 'Reports')

        if not os.path.exists(self._path_to_test_results):
            self.__logger.warning("Tests reports wasn't found.", 'PathService.configure()')
            self._path_to_test_results = None

    def get_path_to_test_results(self, mode='classifier', classifier_name='NBC'):
        if classifier_name not in self._possible_classifiers:
            self.__logger.warning('Got incorrect classifier name.', 'PathService.get_path_to_model()')
            classifier_name = 'NBC'

        if classifier_name not in self._possible_test_results_modes:
            self.__logger.warning('Got incorrect mode.', 'PathService.get_path_to_test_results()')
            return self._path_to_test_results

        if mode.lower().strip() == 'vec_model':
            return os.path.join(self._path_to_test_results, 'VectorModel')

        elif mode.lower().strip() == 'classifier_main':
            return os.path.join(self._path_to_test_results, '..', '..', 'MainReports', 'Classifier', classifier_name)

        elif mode.lower().strip() == 'classifier':
            return self._path_to_test_results

    def get_path_to_model(self, model='unigrams', classifier_name='NBC'):
        if classifier_name not in self._possible_classifiers:
            self.__logger.warning('Got incorrect classifier name.', 'PathService.get_path_to_model()')
            classifier_name = 'NBC'

        if model not in self._possible_model_types:
            self.__logger.warning('Got incorrect model type.', 'PathService.get_path_to_model()')
            model = 'unigrams'

        path_to_models = os.path.join(self._path_to_classifier_models, classifier_name)

        if os.path.exists(path_to_models):
            path_to_required_model = os.path.join(path_to_models, 'model_%s.pkl' % model)

            if os.path.exists(path_to_required_model):
                return path_to_required_model

    def get_path_to_database(self, database_name='unigrams.db'):
        if database_name not in self._possible_databases:
            self.__logger.warning('Got incorrect database name.', 'PathService.get_path_to_database()')
            database_name = 'unigrams.db'

        path_to_database = os.path.join(self.path_to_databases, database_name)

        if os.path.exists(path_to_database):
            return path_to_database

    def get_path_to_dataset(self, dataset):
        if dataset not in self._possible_datasets:
            self.__logger.warning('Got incorrect dataset name.', 'PathService.get_path_to_dataset()')
            dataset = 'dataset_with_unigrams.csv'

        path_to_dataset = os.path.join(self.path_to_databases, dataset)

        if os.path.exists(path_to_dataset):
            return path_to_dataset

    def set_path_to_vector_model(self, path_to_vector_model):
        self.path_to_vector_model = path_to_vector_model
