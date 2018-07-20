# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import sys
import os
import logging
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication, QPushButton, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtGui import QFont, QIcon
from Python.Modules.CountTextTonal.CountTextTonal import Document
from Python.Services.SpeechRecognizer import SpeechRecognizer
from Python.Services.Logger import Logger
import platform
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim

system = platform.system().lower()

# create method "load_vector_model"
if os.getcwd().endswith('Master') and os.path.exists(os.path.join('..', '..', 'Databases',
                                                        'ruscorpora_upos_skipgram_300_10_2017.bin.gz')):

    vec_model = gensim.models.KeyedVectors.load_word2vec_format(os.path.join('..', '..', 'Databases',
                                                        'ruscorpora_upos_skipgram_300_10_2017.bin.gz'), binary=True)

else:
    vec_model = None
    logging.error('\nvector model lost\n')


class MainProgramWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Services
        self.speech_recognizer = SpeechRecognizer()
        self.logger = Logger()

        # GUI Elements
        self.qle = self.qle = QLineEdit(self)
        self.lbl_answ = QLabel(self)
        self.voice_button = QPushButton(self)
        self.answer_button = QPushButton(self)
        self.file_dialog_button = QPushButton(self)
        self.delete_button = QPushButton(self)
        self.message_box = QMessageBox()

        self.logger.configure()

    def launch(self):
        self.setWindowIcon(QIcon('icon.ico'))
        self.setWindowTitle('Sentiment Analyser')

        # create method for configure system for OS

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

            self.file_dialog_button.setText('📂')
            self.file_dialog_button.resize(67, 30)
            self.file_dialog_button.setFont(QFont('Times', 17))
            self.file_dialog_button.move(415, 77)
            self.file_dialog_button.setToolTip('Push to open file')
            self.file_dialog_button.setStyleSheet("""
                                    QPushButton:!hover { background-color: rgb(181, 225, 174) }
                                    QPushButton:hover { background-color: rgb(207, 236, 207) }
                                    QPushButton:pressed { background-color: rgb(145, 210, 144); }
                                """)
            self.file_dialog_button.clicked.connect(self.file_dialog_button_clicked)


        elif system == 'darwin':
            self.setFixedSize(600, 350)
            self.setStyleSheet('QWidget { background-color: rgb(255, 230, 210) }')

            self.qle.resize(460, 40)
            self.qle.setStyleSheet('QWidget { background-color: rgb(255, 255, 255) }')
            self.qle.move(30, 40)
            self.qle.setToolTip('Enter the text here')
            self.qle.setFont(QFont('Times', 24))
            self.qle.returnPressed.connect(self.answer_button_clicked)

            self.lbl_answ.move(180, 180)
            self.lbl_answ.setFont(QFont('Times', 40))
            self.lbl_answ.resize(300, 100)

            self.answer_button.setText('Start')
            self.answer_button.setStyleSheet("""
                QPushButton:hover { background-color: rgb(144, 235, 235) }
                QPushButton:!hover { background-color: rgb(134, 227, 227) }
                QPushButton:pressed { background-color: rgb(124, 218, 217); }
            """)
            self.answer_button.resize(190, 60)
            self.answer_button.move(205, 100)
            self.answer_button.setFont(QFont('Times', 30))
            self.answer_button.setToolTip('Push to count tonal')
            self.answer_button.clicked.connect(self.answer_button_clicked)

            self.voice_button.setText('🎙')
            self.voice_button.resize(40, 40)
            self.voice_button.setFont(QFont('Times', 28))
            self.voice_button.move(500, 40)
            self.voice_button.setToolTip('Push to enter the text by speech')
            self.voice_button.setStyleSheet("""
                QPushButton:hover { background-color: rgb(177, 137, 255) }
                QPushButton:!hover { background-color: rgb(172, 132, 250) }
                QPushButton:pressed { background-color: rgb(155, 118, 245); }
            """)
            self.voice_button.clicked.connect(self.voice_button_clicked)

            self.delete_button.setText('✗')
            self.delete_button.resize(40, 40)
            self.delete_button.setFont(QFont('Times', 28))
            self.delete_button.move(545, 40)
            self.delete_button.setToolTip('Push to clear text box')
            self.delete_button.setStyleSheet("""
                        QPushButton:!hover { background-color: rgb(180, 180, 180) }
                        QPushButton:hover { background-color: rgb(200, 200, 200) }
                        QPushButton:pressed { background-color: rgb(160, 160, 160); }
                    """)
            self.delete_button.clicked.connect(self.delete_button_clicked)

            self.file_dialog_button.setText('📂')
            self.file_dialog_button.resize(85, 40)
            self.file_dialog_button.setFont(QFont('Times', 17))
            self.file_dialog_button.move(500, 85)
            self.file_dialog_button.setToolTip('Push to open file')
            self.file_dialog_button.setStyleSheet("""
                                                QPushButton:!hover { background-color: rgb(181, 225, 174) }
                                                QPushButton:hover { background-color: rgb(207, 236, 207) }
                                                QPushButton:pressed { background-color: rgb(145, 210, 144); }
                                            """)
            self.file_dialog_button.clicked.connect(self.file_dialog_button_clicked)

        self.show()

    def delete_button_clicked(self):
        self.qle.clear()
        self.lbl_answ.clear()

    def voice_button_clicked(self):
        self.message_box.question(self, 'Speak', 'You can start speeking', QMessageBox.Ok)

        voice_text = self.speech_recognizer.recognize_speech()

        if voice_text == 'Unknown value':
            try_again = QMessageBox.Yes

            while try_again == QMessageBox.Yes and voice_text == 'Unknown value':
                try_again = self.message_box.question(self, 'Error', 'Unknown value\n Try again?',
                                                    QMessageBox.Yes | QMessageBox.No)
                if try_again == QMessageBox.No:
                    break

                voice_text = self.speech_recognizer.recognize_speech()

        # method for SpeechRecognizer checking
        if voice_text == 'Internet connection lost':
            self.message_box.question(self, 'Error', 'Internet connection lost', QMessageBox.Ok)
            return None

        if voice_text == 'No microphone':
            self.message_box.question(self, 'Error', 'Microphone was disconnected', QMessageBox.Ok)
            return None

        if voice_text != 'Unknown value':
            self.qle.setText(voice_text)

            return None

    def file_dialog_button_clicked(self):
        # class FileReader
        file_name = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        if file_name:
            with open(file_name, 'r') as file:
                data = file.read()
                self.qle.setText(data)

    def answer_button_clicked(self):
        doc = Document(self.qle.text(), vec_model)
        doc.count_tonal()

        if system == 'windows':
            # method for configure answer label on Windows
            if doc.tonal == 'positive':
                self.lbl_answ.setStyleSheet('QLabel {color:rgba(0, 200, 100, 255)}')
                self.lbl_answ.move(193.5, 180)

            elif doc.tonal == 'negative':
                self.lbl_answ.setStyleSheet('QLabel {color:rgba(255, 56, 20, 255)}')
                self.lbl_answ.move(180, 180)

        elif system == 'darwin':
            # method for configure answer label on Darwin
            if doc.tonal == 'positive':
                self.lbl_answ.setStyleSheet('QLabel {color:rgba(0, 200, 100, 255)}')
                self.lbl_answ.move(230, 210)

            elif doc.tonal == 'negative':
                self.lbl_answ.setStyleSheet('QLabel {color:rgba(255, 56, 20, 255)}')
                self.lbl_answ.move(225, 210)

        self.lbl_answ.setToolTip('Tonal and probability')

        if doc.probability:
            self.lbl_answ.setText(doc.tonal.capitalize() + '\n' + str(round(doc.probability * 100, 3)) + '%')
        else:
            self.lbl_answ.setText(doc.tonal.capitalize())


app = QApplication(sys.argv)
main_window = MainProgramWindow()
main_window.launch()

sys.exit(app.exec_())
