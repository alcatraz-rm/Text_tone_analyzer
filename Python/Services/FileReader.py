# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import sys
import os
import chardet
from PyQt5.QtWidgets import QFileDialog, QWidget
sys.path.append(os.path.join('..', '..'))

from Python.Services.Logger import Logger


class FileReader(QWidget):
    def __init__(self):
        super().__init__()
        self.logger = Logger()

        if not self.logger.configured:
            self.logger.configure()

        self.file_dialog = QFileDialog()

        self.logger.info('FileReader was successfully initialized.', 'FileReader.__init__()')

    def detect_encoding(self, filename):
        with open(filename, 'rb') as byte_file:
            byte_string = byte_file.read()

        encoding = chardet.detect(byte_string)['encoding']

        self.logger.info('file encoding: %s' % encoding, 'FileReader.detect_encoding()')

        return encoding

    def get_file_content(self):
        data = None

        try:
            filename = self.file_dialog.getOpenFileName(self, 'Open file', '/home')[0]
            self.logger.info('filename: %s' % filename, 'FileReader.get_file_content()')

            if filename:
                with open(filename, 'r', encoding=self.detect_encoding(filename)) as file:
                    data = file.read()

        except SystemError:
            self.logger.error('System error.', 'FileReader.get_file_content()')

        return data
