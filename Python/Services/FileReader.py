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

import chardet
from PyQt5.QtWidgets import QFileDialog, QWidget

from Python.Services.Logger import Logger


class FileReader(QWidget):
    def __init__(self):
        super().__init__()
        self.__logger = Logger()
        self.__file_dialog = QFileDialog()

        self.__logger.info('FileReader was successfully initialized.', __name__)

    def _detect_encoding(self, filename: str):
        with open(filename, 'rb') as byte_file:
            byte_string = byte_file.read()

        encoding = chardet.detect(byte_string)['encoding']

        self.__logger.info(f"File's encoding: {encoding}", __name__)

        return encoding

    def get_file_content(self):
        try:
            filename = self.__file_dialog.getOpenFileName(self, 'Open file', '/home')[0]
            self.__logger.info(f'Filename: {filename}', __name__)

            if filename:
                with open(filename, 'r', encoding=self._detect_encoding(filename)) as file:
                    return file.read()

        except BaseException as exception:
            self.__logger.error(str(exception), __name__)
