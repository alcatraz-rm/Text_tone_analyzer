# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import sys
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
        self.setWindowIcon(QIcon('icon.ico'))
        self.setWindowTitle('Sentiment Analyser')
        self.setGeometry(500, 500, 500, 300)
        self.setStyleSheet("QWidget { background-color: rgb(43, 43, 43) }")

        self.qle = QLineEdit(self)
        self.qle.resize(375, 30)
        self.qle.setStyleSheet("QWidget { background-color: rgb(255, 255, 255) }")
        self.qle.move(62.5, 40)
        self.qle.setFont(QFont("Times", 14))

        # self.lbl = QLabel(self)
        # self.lbl.move(15, 37)
        # self.lbl.setFont(QFont("Times", 14))
        # self.lbl.resize(200, 30)
        # self.lbl.setText('Text:')

        self.lbl_answ = QLabel(self)
        self.lbl_answ.move(180, 180)
        self.lbl_answ.setFont(QFont("Times", 24))
        self.lbl_answ.resize(300, 100)

        self.btn = QPushButton("", self)
        self.btn.setStyleSheet("""
            QPushButton:hover { background-color: rgb(200, 34, 0) }
            QPushButton:!hover { background-color: rgb(224, 34, 0) }
            QPushButton:pressed { background-color: rgb(180, 34, 0); }
        """)
        self.btn.resize(190, 60)
        self.btn.move(155, 100)
        self.btn.setFont(QFont("Times", 12))
        self.btn.clicked.connect(self.button_clicked)

        self.show()

    def button_clicked(self):
        logging.info('entered text: %s' % self.qle.text())
        doc = Document(self.qle.text())
        doc.count_tonal()

        if doc.tonal == 'positive':
            self.lbl_answ.setStyleSheet("QLabel {color:rgba(55, 173, 95, 255)}")
            self.lbl_answ.move(193.5, 180)
        elif doc.tonal == 'negative':
            self.lbl_answ.setStyleSheet("QLabel {color:rgba(255, 56, 20, 255)}")
            self.lbl_answ.move(180, 180)

        self.lbl_answ.setText(doc.tonal.capitalize())


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

