# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import platform
import sys
import os
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication, QPushButton, QMessageBox, QFileDialog
sys.path.append(os.path.join('..', '..'))

from Python.Services.Logger import Logger
from Python.Services.SpeechRecognizer import SpeechRecognizer
from Python.Master.TextTonalAnalyzer import TextTonalAnalyzer
from Python.Services.FileReader import FileReader


class MainProgramWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.os = platform.system().lower()

        # Services
        self.speech_recognizer = SpeechRecognizer()
        self.file_reader = FileReader()
        self.logger = Logger()
        self.text_tonal_analyzer = TextTonalAnalyzer()

        self.logger.configure()

        # GUI Elements
        self.line_edit = QLineEdit(self)
        self.answer_label = QLabel(self)
        self.voice_button = QPushButton(self)
        self.answer_button = QPushButton(self)
        self.file_dialog_button = QPushButton(self)
        self.delete_button = QPushButton(self)
        self.message_box = QMessageBox()

    def configure_main_window(self):
        self.set_base_params()
        self.configure_line_edit()
        self.configure_answer_button()
        self.configure_voice_button()
        self.configure_delete_button()
        self.configure_file_dialog_button()
        self.configure_answer_label()

    def set_base_params(self):
        if self.os == 'windows':
            self.setFixedSize(500, 300)
            self.setStyleSheet('QWidget { background-color: rgb(255, 222, 200) }')

        elif self.os == 'darwin':
            self.setFixedSize(600, 350)
            self.setStyleSheet('QWidget { background-color: rgb(255, 230, 210) }')

    def configure_line_edit(self):
        self.line_edit.setToolTip('Enter the text here')
        self.line_edit.returnPressed.connect(self.answer_button_clicked)

        if self.os == 'windows':
            self.line_edit.resize(375, 30)
            self.line_edit.setStyleSheet('QWidget { background-color: rgb(255, 255, 255) }')
            self.line_edit.move(32.5, 40)
            self.line_edit.setFont(QFont('Times', 14))

        elif self.os == 'darwin':
            self.line_edit.resize(460, 40)
            self.line_edit.setStyleSheet('QWidget { background-color: rgb(255, 255, 255) }')
            self.line_edit.move(30, 40)
            self.line_edit.setFont(QFont('Times', 24))

    def configure_answer_button(self):
        self.answer_button.clicked.connect(self.answer_button_clicked)
        self.answer_button.setText('Start')
        self.answer_button.setToolTip('Push to count tonal')

        if self.os == 'windows':
            self.answer_button.setStyleSheet("""
                            QPushButton:hover { background-color: rgb(144, 235, 235) }
                            QPushButton:!hover { background-color: rgb(134, 227, 227) }
                            QPushButton:pressed { background-color: rgb(124, 218, 217); }
                        """)
            self.answer_button.resize(190, 60)
            self.answer_button.move(155, 100)
            self.answer_button.setFont(QFont('Times', 17))

        elif self.os == 'darwin':
            self.answer_button.setStyleSheet("""
                QPushButton:hover { background-color: rgb(144, 235, 235) }
                QPushButton:!hover { background-color: rgb(134, 227, 227) }
                QPushButton:pressed { background-color: rgb(124, 218, 217); }
            """)
            self.answer_button.resize(190, 60)
            self.answer_button.move(205, 100)
            self.answer_button.setFont(QFont('Times', 30))

    def configure_voice_button(self):
        self.voice_button.setText('🎙')
        self.voice_button.setToolTip('Push to enter the text by speech')
        self.voice_button.clicked.connect(self.voice_button_clicked)

        if self.os == 'windows':
            self.voice_button.resize(30, 30)
            self.voice_button.setFont(QFont('Times', 17))
            self.voice_button.move(415, 40)
            self.voice_button.setStyleSheet("""
                            QPushButton:hover { background-color: rgb(177, 137, 255) }
                            QPushButton:!hover { background-color: rgb(172, 132, 250) }
                            QPushButton:pressed { background-color: rgb(155, 118, 245); }
                        """)

        elif self.os == 'darwin':
            self.voice_button.resize(40, 40)
            self.voice_button.setFont(QFont('Times', 28))
            self.voice_button.move(500, 40)
            self.voice_button.setStyleSheet("""
                QPushButton:hover { background-color: rgb(177, 137, 255) }
                QPushButton:!hover { background-color: rgb(172, 132, 250) }
                QPushButton:pressed { background-color: rgb(155, 118, 245); }
            """)

    def configure_delete_button(self):
        self.delete_button.setText('✗')
        self.delete_button.setToolTip('Push to clear text box')
        self.delete_button.clicked.connect(self.delete_button_clicked)

        if self.os == 'windows':
            self.delete_button.resize(30, 30)
            self.delete_button.setFont(QFont('Times', 17))
            self.delete_button.move(452, 40)
            self.delete_button.setStyleSheet("""
                                    QPushButton:!hover { background-color: rgb(180, 180, 180) }
                                    QPushButton:hover { background-color: rgb(200, 200, 200) }
                                    QPushButton:pressed { background-color: rgb(160, 160, 160); }
                                """)

        elif self.os == 'darwin':
            self.delete_button.resize(40, 40)
            self.delete_button.setFont(QFont('Times', 28))
            self.delete_button.move(545, 40)
            self.delete_button.setStyleSheet("""
                        QPushButton:!hover { background-color: rgb(180, 180, 180) }
                        QPushButton:hover { background-color: rgb(200, 200, 200) }
                        QPushButton:pressed { background-color: rgb(160, 160, 160); }
                    """)

    def configure_file_dialog_button(self):
        self.file_dialog_button.setText('📂')
        self.file_dialog_button.setToolTip('Push to open file')
        self.file_dialog_button.clicked.connect(self.file_dialog_button_clicked)

        if self.os == 'windows':
            self.file_dialog_button.resize(67, 30)
            self.file_dialog_button.setFont(QFont('Times', 17))
            self.file_dialog_button.move(415, 77)
            self.file_dialog_button.setStyleSheet("""
                                                QPushButton:!hover { background-color: rgb(181, 225, 174) }
                                                QPushButton:hover { background-color: rgb(207, 236, 207) }
                                                QPushButton:pressed { background-color: rgb(145, 210, 144); }
                                            """)

        elif self.os == 'darwin':
            self.file_dialog_button.resize(85, 40)
            self.file_dialog_button.setFont(QFont('Times', 17))
            self.file_dialog_button.move(500, 85)
            self.file_dialog_button.setStyleSheet("""
                                                QPushButton:!hover { background-color: rgb(181, 225, 174) }
                                                QPushButton:hover { background-color: rgb(207, 236, 207) }
                                                QPushButton:pressed { background-color: rgb(145, 210, 144); }
                                            """)

    def configure_answer_label(self):
        if self.os == 'windows':
            self.answer_label.move(180, 180)
            self.answer_label.setFont(QFont('Times', 24))
            self.answer_label.resize(300, 100)

        elif self.os == 'darwin':
            self.answer_label.move(180, 180)
            self.answer_label.setFont(QFont('Times', 40))
            self.answer_label.resize(300, 100)

    def launch(self):
        self.setWindowIcon(QIcon('icon.ico'))
        self.setWindowTitle('Sentiment Analyser')

        self.configure_main_window()
        self.show()

    def delete_button_clicked(self):
        self.line_edit.clear()
        self.answer_label.clear()

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

        if voice_text == 'Internet connection lost':
            self.message_box.question(self, 'Error', 'Internet connection lost', QMessageBox.Ok)
            return None

        if voice_text == 'No microphone':
            self.message_box.question(self, 'Error', 'Microphone was disconnected', QMessageBox.Ok)
            return None

        if voice_text != 'Unknown value':
            self.line_edit.setText(voice_text)

            return None

    def file_dialog_button_clicked(self):
        file_content = self.file_reader.get_file_content()
        if file_content:
            self.line_edit.setText(file_content)

    def answer_button_clicked(self):
        self.text_tonal_analyzer.detect_tonal(self.line_edit.text())

        if self.os == 'windows':
            if self.text_tonal_analyzer.tonal == 'positive':
                self.answer_label.setStyleSheet('QLabel {color:rgba(0, 200, 100, 255)}')
                self.answer_label.move(193.5, 180)

            elif self.text_tonal_analyzer.tonal == 'negative':
                self.answer_label.setStyleSheet('QLabel {color:rgba(255, 56, 20, 255)}')
                self.answer_label.move(180, 180)

        elif self.os == 'darwin':
            if self.text_tonal_analyzer.tonal == 'positive':
                self.answer_label.setStyleSheet('QLabel {color:rgba(0, 200, 100, 255)}')
                self.answer_label.move(230, 210)

            elif self.text_tonal_analyzer.tonal == 'negative':
                self.answer_label.setStyleSheet('QLabel {color:rgba(255, 56, 20, 255)}')
                self.answer_label.move(225, 210)

        self.answer_label.setToolTip('Tonal and probability')

        if self.text_tonal_analyzer.probability:
            self.answer_label.setText(self.text_tonal_analyzer.tonal.capitalize() + '\n' +
                                      str(round(self.text_tonal_analyzer.probability * 100, 3)) + '%')
        else:
            self.answer_label.setText(self.text_tonal_analyzer.tonal.capitalize())


app = QApplication(sys.argv)
main_window = MainProgramWindow()
main_window.launch()

sys.exit(app.exec_())
