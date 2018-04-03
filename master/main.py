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
from modules.voice.recognition import recognize_speech, check_microphone
import platform

system = platform.system().lower()

if not os.path.exists('logs'):
    os.mkdir('logs')

time = str(datetime.datetime.now()).replace(':', '-')
logging.basicConfig(filename=os.path.join('logs', 'log_%s.log' % time), filemode='w', level=logging.INFO)
logging.info('\nmain\n')
logging.info('\noperation system: %s\n' % system)


class MainProgramWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.qle = self.qle = QLineEdit(self)
        self.lbl_answ = QLabel(self)
        self.voice_button = QPushButton(self)
        self.answer_button = QPushButton(self)
        self.unknown_value_message = QMessageBox()
        self.internet_lost_message = QMessageBox()
        self.delete_button = QPushButton(self)
        self.speak_message = QMessageBox()
        self.no_microphone_message = QMessageBox()

        self.main()

    def main(self):
        self.setWindowIcon(QIcon('icon.ico'))
        self.setWindowTitle('Sentiment Analyser')

        if system == 'windows':
            self.setFixedSize(500, 300)
            self.setStyleSheet('QWidget { background-color: rgb(255, 222, 200) }')

            self.qle.resize(375, 30)
            self.qle.setStyleSheet('QWidget { background-color: rgb(255, 255, 255) }')
            self.qle.move(32.5, 40)
            self.qle.setToolTip('Enter the text here')
            self.qle.setFont(QFont('Times', 14))
            self.qle.returnPressed.connect(self.answer_button_clicked)

            self.lbl_answ.move(180, 180)
            self.lbl_answ.setFont(QFont('Times', 24))
            self.lbl_answ.resize(300, 100)

            self.answer_button.setText('Start')
            self.answer_button.setStyleSheet("""
                QPushButton:hover { background-color: rgb(144, 235, 235) }
                QPushButton:!hover { background-color: rgb(134, 227, 227) }
                QPushButton:pressed { background-color: rgb(124, 218, 217); }
            """)
            self.answer_button.resize(190, 60)
            self.answer_button.move(155, 100)
            self.answer_button.setFont(QFont('Times', 17))
            self.answer_button.setToolTip('Push to count tonal')
            self.answer_button.clicked.connect(self.answer_button_clicked)

            self.voice_button.setText('🎙')
            self.voice_button.resize(30, 30)
            self.voice_button.setFont(QFont('Times', 17))
            self.voice_button.move(415, 40)
            self.voice_button.setToolTip('Push to enter the text by speech')
            self.voice_button.setStyleSheet("""
                QPushButton:hover { background-color: rgb(177, 137, 255) }
                QPushButton:!hover { background-color: rgb(172, 132, 250) }
                QPushButton:pressed { background-color: rgb(155, 118, 245); }
            """)
            self.voice_button.clicked.connect(self.voice_button_clicked)

            self.delete_button.setText('✗')
            self.delete_button.resize(30, 30)
            self.delete_button.setFont(QFont('Times', 17))
            self.delete_button.move(452, 40)
            self.delete_button.setToolTip('Push to clear text box')
            self.delete_button.setStyleSheet("""
                        QPushButton:!hover { background-color: rgb(180, 180, 180) }
                        QPushButton:hover { background-color: rgb(200, 200, 200) }
                        QPushButton:pressed { background-color: rgb(160, 160, 160); }
                    """)
            self.delete_button.clicked.connect(self.delete_button_clicked)

            self.show()

        elif system == 'darwin':
            pass

    def delete_button_clicked(self):
        self.qle.clear()
        self.lbl_answ.clear()

    def voice_button_clicked(self):
        if check_microphone():
            self.speak_message.question(self, 'Speak', 'You can start speeking', QMessageBox.Ok)
            if self.speak_message:
                voice_text = recognize_speech()

                if voice_text == 'Unknown value':
                    while self.unknown_value_message.question(self, 'Error', 'Unknown value\nTry again?',
                                                           QMessageBox.Yes | QMessageBox.No):
                        voice_text = recognize_speech()
                        if voice_text != 'Unknown value':
                            break

                if voice_text == 'Internet connection lost':
                    self.internet_lost_message.question(self, 'Error', 'Internet connection lost', QMessageBox.Ok)
                    return ''

                if voice_text == 'No microphone':
                    self.no_microphone_message.question(self, 'Error', 'Microphone was disconnected', QMessageBox.Ok)
                    return ''

                self.qle.setText(voice_text)
        else:
            self.no_microphone_message.question(self, 'Error', 'No microphone \nPlease, connect and try again',
                                                 QMessageBox.Ok)
            return ''

    def answer_button_clicked(self):
        logging.info('entered text: %s' % self.qle.text())
        doc = Document(self.qle.text())
        doc.count_tonal()

        if system == 'windows':
            if doc.tonal == 'positive':
                self.lbl_answ.setStyleSheet('QLabel {color:rgba(0, 200, 100, 255)}')
                self.lbl_answ.move(193.5, 180)
            elif doc.tonal == 'negative':
                self.lbl_answ.setStyleSheet('QLabel {color:rgba(255, 56, 20, 255)}')
                self.lbl_answ.move(180, 180)

        self.lbl_answ.setToolTip('Tonal and probability')
        self.lbl_answ.setText(doc.tonal.capitalize() + '\n' + str(round(doc.probability * 100, 3)) + '%')


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

