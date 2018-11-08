import operator

from sklearn.externals import joblib

from Python.Services.Logger import Logger
from Python.Services.PathService import PathService


class TfIdfVectorizer:
    def __init__(self):
        self.__logger = Logger()
        self._path_service = PathService()
        self._vectorizer = None
        self.__logger.info('TfIdf Vectorizer was successfully initialized.', __name__)

        self._load_model()

    def _load_model(self):
        self._vectorizer = joblib.load(self._path_service.path_to_vectorizer)

    def transform(self, text):
        pass

    def _extract_keywords(self, text: str):
        keys = dict()
        result = dict()

        for item in text.split():
            tmp = self._vectorizer.transform([item])

            if tmp.data:
                key = tmp.indices[0]

                keys[key] = item

        data = self._vectorizer.transform([text])
        indices = list(data.indices)
        values = list(data.data)

        data = {indices[i]: values[i] for i in range(len(indices))}

        for key in keys:
            result[keys[key]] = data[key]

        result = sorted(result.items(), key=operator.itemgetter(1))

        if len(result) // 3 == 0:
            return [result[-1][0]]
        else:
            return [item[0] for item in result[(len(result) - len(result) // 3):]]

    def __del__(self):
        del self._path_service
        del self._vectorizer
        del self.__logger
