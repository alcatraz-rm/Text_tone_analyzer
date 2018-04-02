# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import sys
import json
import os
import logging
import datetime
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication, QPushButton, QComboBox, QMainWindow, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from modules.count_text_tonal.count_text_tonal import Document

if not os.path.exists('logs'):
    os.mkdir('logs')

time = str(datetime.datetime.now()).replace(':', '-')
logging.basicConfig(filename=os.path.join('logs', 'log_%s.log' % time), filemode='w', level=logging.INFO)
logging.info('\nmain\n')


class MainProgramWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.main()

    def main(self):
        self.config = 2
        self.setWindowIcon(QIcon('icon.ico'))
        self.setWindowTitle('Sentiment Analyser')

        self.setGeometry(1000, 1000, 1000, 1000)

        self.qle = QLineEdit(self)
        self.qle.resize(750, 60)
        self.qle.move(125, 175)
        self.qle.setFont(QFont("Times", 30))

        self.lbl_answ = QLabel(self)
        self.lbl_answ.move(125, 350)
        self.lbl_answ.setFont(QFont("Times", 40))
        self.lbl_answ.resize(750, 200)

        self.btn = QPushButton("Посчитать тональность", self)
        self.btn.resize(600, 80)
        self.btn.move(200, 250)
        self.btn.setFont(QFont("Times", 24))
        self.btn.clicked.connect(self.button_clicked)

        self.show()

    def button_clicked(self):
        logging.info('entered text: %s' % self.qle.text())
        doc = Document(self.qle.text())
        doc.count_tonal()
        self.lbl_answ.setText('Tonal: %s' % doc.tonal)


class Main(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.main_window = None
        self.main()

    def main(self):
        self.main_window = MainProgramWindow()


app = QApplication(sys.argv)
main = Main()
sys.exit(app.exec_())

