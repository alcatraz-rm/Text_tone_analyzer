# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import chardet
from PyQt5.QtWidgets import QFileDialog, QWidget
from Python.Services.Logger import Logger


class FileReader(QWidget):
    def __init__(self):
        super().__init__()
        self.__logger = Logger()

        if not self.__logger.configured:
            self.__logger.configure()

        self.__file_dialog = QFileDialog()

        self.__logger.info('FileReader was successfully initialized.', 'FileReader.__init__()')

    def _detect_encoding(self, filename):
        with open(filename, 'rb') as byte_file:
            byte_string = byte_file.read()

        encoding = chardet.detect(byte_string)['encoding']

        self.__logger.info("File's encoding: %s" % encoding, 'FileReader._detect_encoding()')

        return encoding

    def get_file_content(self):
        data = None

        try:
            filename = self.__file_dialog.getOpenFileName(self, 'Open file', '/home')[0]
            self.__logger.info('Filename: %s' % filename, 'FileReader.get_file_content()')

            if filename:
                with open(filename, 'r', encoding=self._detect_encoding(filename)) as file:
                    data = file.read()

        except SystemError:
            self.__logger.error('System error.', 'FileReader.get_file_content()')

        return data
