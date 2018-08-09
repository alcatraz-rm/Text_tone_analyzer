import os


class PathService:
    def __init__(self):
        self._cwd = os.getcwd()
        self._path_to_databases = None

        self.path_to_unigrams_database = None
        self.path_to_bigrams_database = None
        self.path_to_trigrams_database = None

        self.path_to_vector_model = None
        self.path_to_models = None

    def _find_databases(self):
        pass
    
    def configure(self):
        pass

    def get_path_to_model(self, classifier_name, model):
        pass
