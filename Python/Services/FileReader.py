# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import sys
import os
import chardet
sys.path.append(os.path.join('..', '..'))

from PyQt5.QtWidgets import QFileDialog, QWidget


class FileReader(QWidget):
    def __init__(self):
        super().__init__()
        self.file_dialog = QFileDialog()

    @staticmethod
    def detect_encoding(filename):
        with open(filename, 'rb') as byte_file:
            byte_string = byte_file.read()

        return chardet.detect(byte_string)['encoding']

    def get_file_content(self):
        data = None
        try:
            filename = self.file_dialog.getOpenFileName(self, 'Open file', '/home')[0]
            if filename:
                with open(filename, 'r', encoding=self.detect_encoding(filename)) as file:
                    data = file.read()
        except SystemError:
            pass

        return data
