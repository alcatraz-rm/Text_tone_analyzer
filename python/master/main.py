# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import sys
sys.path.append('..')
import os
import logging
import datetime
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication, QPushButton, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtGui import QFont, QIcon
from python.modules.count_text_tonal.count_text_tonal import Document
from python.modules.voice.recognition import recognize_speech, check_microphone
import platform
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim

# class Logger
system = platform.system().lower()
cwd = os.getcwd()

time = str(datetime.datetime.now()).replace(':', '-')
logging.basicConfig(filename=os.path.join('logs', 'log_%s.log' % time), filemode='w', level=logging.INFO)
logging.info('\nmain\n')
logging.info('\noperation system: %s\n' % system)
logging.info('\nCWD: %s' % cwd)


# create method "load_vector_model"
if cwd.endswith('master') and os.path.exists(os.path.join('..', '..', 'databases',
                                                        'ruscorpora_upos_skipgram_300_10_2017.bin.gz')):

    vec_model = gensim.models.KeyedVectors.load_word2vec_format(os.path.join('..', '..', 'databases',
                                                        'ruscorpora_upos_skipgram_300_10_2017.bin.gz'), binary=True)

else:
    vec_model = None
    logging.error('\nvector model lost\n')

if not os.path.exists('logs'):
    os.mkdir('logs')


class MainProgramWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.qle = self.qle = QLineEdit(self)
        self.lbl_answ = QLabel(self)
        self.voice_button = QPushButton(self)
        self.answer_button = QPushButton(self)
        self.file_dialog_button = QPushButton(self)
        self.unknown_value_message = QMessageBox()
        self.internet_lost_message = QMessageBox()
        self.delete_button = QPushButton(self)
        self.speak_message = QMessageBox()
        self.no_microphone_message = QMessageBox()

        # Rename to launch(), don't call in constructor
        self.main()

    def main(self):
        self.setWindowIcon(QIcon('icon.ico'))
        self.setWindowTitle('Sentiment Analyser')

        # create file with system params (OS, WD, DateTime)
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
        # class SpeechListener
        if check_microphone():
            self.speak_message.question(self, 'Speak', 'You can start speeking', QMessageBox.Ok)

            if self.speak_message:
                voice_text = recognize_speech()

                if voice_text == 'Unknown value':
                    answer = self.unknown_value_message.question(self, 'Error', 'Unknown value\nTry again?',
                                                           QMessageBox.Yes | QMessageBox.No)

                    """
                    QMessageBox().question(self, text, QMessageBox.Yes | QMessageBox.No) returns 65536 if user pushed "No"
                    and 16384 if user pushed "Yes"
                    """

                    # magic numbers
                    if answer == QMessageBox.No:
                        answer = False
                    elif answer == QMessageBox.Yes:
                        answer = True

                    if answer:
                        while answer:
                            voice_text = recognize_speech()

                            if voice_text != 'Unknown value':
                                break

                            answer = self.unknown_value_message.question(self, 'Error', 'Unknown value\nTry again?',
                                                                QMessageBox.Yes | QMessageBox.No)

                            # magic numbers
                            if answer == QMessageBox.No:
                                answer = False
                            elif answer == QMessageBox.Yes:
                                answer = True
                    else:
                        return None

                # method for voice checking
                if voice_text == 'Internet connection lost':
                    self.internet_lost_message.question(self, 'Error', 'Internet connection lost', QMessageBox.Ok)
                    return None

                if voice_text == 'No microphone':
                    self.no_microphone_message.question(self, 'Error', 'Microphone was disconnected', QMessageBox.Ok)
                    return None

                if voice_text != 'Unknown value':
                    self.qle.setText(voice_text)
        else:
            self.no_microphone_message.question(self, 'Error', 'No microphone \nPlease, connect it and try again',
                                                 QMessageBox.Ok)

            return None

    def file_dialog_button_clicked(self):
        # class FileReader
        file_name = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        if file_name:
            with open(file_name, 'r') as file:
                data = file.read()
                self.qle.setText(data)

    def answer_button_clicked(self):
        logging.info('entered text: %s' % self.qle.text())
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


# Delete this class
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
