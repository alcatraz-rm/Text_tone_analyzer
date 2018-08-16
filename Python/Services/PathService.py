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

        self.path_to_parts_of_speech = None
        self._path_to_main_directory = None

        self.path_to_vector_model = None
        self._path_to_classifier_models = None

        self._path_to_test_results = None

        self.configure()
        self.__logger.info('PathService was successfully configured.', 'PathService.__init__()')

    def _find_databases(self):
        while not os.getcwd().endswith('Python'):
            os.chdir('..')

        self._path_to_main_directory = os.getcwd()

        self.path_to_databases = os.path.abspath(os.path.join('..', 'Databases'))
        os.chdir(self._cwd)

    def configure(self):
        self._find_databases()

        self.path_to_vector_model = os.path.join(self.path_to_databases, 'ruscorpora_upos_skipgram_300_10_2017.bin.gz')

        if not os.path.exists(self.path_to_vector_model):
            self.path_to_vector_model = None

        self.path_to_parts_of_speech = os.path.join(self._path_to_main_directory, 'Services',
                                                    'Lemmatizer', 'parts_of_speech.json')

        if not os.path.exists(self.path_to_parts_of_speech):
            self.path_to_parts_of_speech = None

        self._path_to_classifier_models = os.path.join(self.path_to_databases, 'Models')
        self._path_to_test_results = os.path.join(self._path_to_main_directory, 'Tests', 'Reports')

    def get_path_to_test_results(self, mode, classifier_name='NBC'):
        if mode == 'vec_model':
            return os.path.join(self._path_to_test_results, 'VectorModel')

        elif mode == 'classifier':
            return os.path.join(self._path_to_test_results, 'Classifier', classifier_name)

    def get_path_to_model(self, classifier_name, model):
        path_to_models = os.path.join(self._path_to_classifier_models, classifier_name)

        if os.path.exists(path_to_models):
            path_to_required_model = os.path.join(path_to_models, 'model_%s.pkl' % model)

            if os.path.exists(path_to_required_model):
                return path_to_required_model

        return None

    def get_path_to_database(self, database_name):
        path_to_database = os.path.join(self.path_to_databases, database_name)

        if os.path.exists(path_to_database):
            return path_to_database
        else:
            return None

    def get_path_to_dataset(self, dataset):
        path_to_dataset = os.path.join(self.path_to_databases, dataset)

        if os.path.exists(path_to_dataset):
            return path_to_dataset

        return None
