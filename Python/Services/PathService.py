import os
from Python.Services.Logger import Logger


class PathService:
    def __init__(self):
        self.__logger = Logger()

        if not self.__logger.configured:
            self.__logger.configure()

        self._cwd = os.getcwd()
        self._path_to_databases = None

        self.path_to_vector_model = None
        self._path_to_classifier_models = None

        self.configure()
        self.__logger.info('PathService was successfully configured.', 'PathService.__init__()')

    def _find_databases(self):
        while not os.getcwd().endswith('Python'):
            os.chdir('..')

        self._path_to_databases = os.path.abspath(os.path.join('..', 'Databases'))
        os.chdir(self._cwd)

    def configure(self):
        self._find_databases()

        self.path_to_vector_model = os.path.join(self._path_to_databases, 'ruscorpora_upos_skipgram_300_10_2017.bin.gz')

        self._path_to_classifier_models = os.path.join(self._path_to_databases, 'Models')

    def get_path_to_model(self, classifier_name, model):
        path_to_models = os.path.join(self._path_to_classifier_models, classifier_name)

        if os.path.exists(path_to_models):
            path_to_required_model = os.path.join(path_to_models, 'model_%s.pkl' % model)

            if os.path.exists(path_to_required_model):
                return path_to_required_model

        return None

    def get_path_to_database(self, database_name):
        path_to_database = os.path.join(self._path_to_databases, database_name)

        if os.path.exists(path_to_database):
            return path_to_database
        else:
            return None
