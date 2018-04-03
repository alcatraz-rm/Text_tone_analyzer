# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import sys
import os
import logging
import datetime
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication, QPushButton, QMainWindow, QMessageBox, QPlainTextEdit
from PyQt5.QtGui import QFont, QIcon
from modules.count_text_tonal.count_text_tonal import Document
from modules.voice.recognition import recognize_speech

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
        self.setStyleSheet("QWidget { background-color: rgb(255, 222, 200) }")

        self.qle = QLineEdit(self)
        self.qle.resize(375, 30)
        self.qle.setStyleSheet("QWidget { background-color: rgb(255, 255, 255) }")
        self.qle.move(62.5, 40)
        self.qle.setFont(QFont("Times", 14))

        self.lbl_answ = QLabel(self)
        self.lbl_answ.move(180, 180)
        self.lbl_answ.setFont(QFont("Times", 24))
        self.lbl_answ.resize(300, 100)

        self.btn = QPushButton("", self)
        self.btn.setStyleSheet("""
            QPushButton:hover { background-color: rgb(144, 235, 235) }
            QPushButton:!hover { background-color: rgb(134, 227, 227) }
            QPushButton:pressed { background-color: rgb(124, 218, 217); }
        """)
        self.btn.resize(190, 60)
        self.btn.move(155, 100)
        self.btn.setFont(QFont('Times', 12))
        self.btn.setToolTip('Push to count tonal')
        self.btn.clicked.connect(self.button_clicked)

        self.voice_btn = QPushButton("🎙", self)
        self.voice_btn.resize(30, 30)
        self.voice_btn.setFont(QFont('Times', 17))
        self.voice_btn.move(30, 40)
        self.voice_btn.setStyleSheet("""
            QPushButton:hover { background-color: rgb(177, 137, 255) }
            QPushButton:!hover { background-color: rgb(172, 132, 250) }
            QPushButton:pressed { background-color: rgb(155, 118, 245); }
        """)
        self.voice_btn.clicked.connect(self.voice_button_clicked)

        self.show()

    def voice_button_clicked(self):
        self.speak_message = QMessageBox()
        self.speak_message.question(self, 'Speak', 'You can start speeking', QMessageBox.Ok)
        if self.speak_message:
            voice_text = recognize_speech()

            if voice_text == 'Unknown value':
                self.unknown_value_message = QMessageBox()
                while self.unknown_value_message.question(self, 'Error', 'Unknown value\nTry again?',
                                                       QMessageBox.Yes | QMessageBox.No):
                    voice_text = recognize_speech()
                    if voice_text != 'Unknown value':
                        break

            if voice_text == 'Internet connection lost':
                self.internet_lost_message = QMessageBox()
                self.internet_lost_message.question(self, 'Error', 'Internet connection lost', QMessageBox.Ok)
                return ''

            self.qle.setText(voice_text)

    def button_clicked(self):
        logging.info('entered text: %s' % self.qle.text())
        doc = Document(self.qle.text())
        doc.count_tonal()

        if doc.tonal == 'positive':
            self.lbl_answ.setStyleSheet("QLabel {color:rgba(0, 200, 100, 255)}")
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

