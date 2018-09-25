# Copyright © 2018. All rights reserved.
# Author: German Yakimov

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import platform
import sys
import os
import json
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication, QPushButton, QMessageBox
sys.path.append('..')

from Python.Services.Logger import Logger
from Python.Services.SpeechRecognizer import SpeechRecognizer
from Python.TextTonalAnalyzer import TextTonalAnalyzer
from Python.Services.FileReader import FileReader
from Python.Services.PathService import PathService


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.os = platform.system().lower()

        # Services
        self._speech_recognizer = SpeechRecognizer()
        self._file_reader = FileReader()
        self.__logger = Logger()
        self._path_service = PathService()
        self._text_tonal_analyzer = TextTonalAnalyzer('NBC')

        if not self.__logger.configured:
            self.__logger.configure()

        self._config = None
        self._load_config()

        # GUI Elements
        self.line_edit = QLineEdit(self)
        self.answer_label = QLabel(self)
        self.voice_button = QPushButton(self)
        self.answer_button = QPushButton(self)
        self.file_dialog_button = QPushButton(self)
        self.delete_button = QPushButton(self)
        self.message_box = QMessageBox()

    def _load_config(self):
        path_to_config = os.path.join(self._path_service.path_to_configs, 'demo.json')

        with open(path_to_config, 'r', encoding='utf-8') as file:
            self._config = json.load(file)

        if self.os == 'windows':
            self._config = self._config['windows']
        else:
            self._config = self._config['darwin']

    def _configure_main_window(self):
        self._set_base_params()

        self._configure_line_edit()
        self._configure_answer_button()
        self.configure_voice_button()
        self._configure_delete_button()
        self._configure_file_dialog_button()
        self._configure_answer_label()

        self.__logger.info('Main window was successfully configured.', 'MainWindow.configure_main_window()')

    def _set_base_params(self):
        self.setFixedSize(*self._config['size'])
        self.setStyleSheet('QWidget { background-color: %s }' % self._config['background-color'])

    def _configure_line_edit(self):
        self.line_edit.setToolTip('Enter the text here')
        self.line_edit.returnPressed.connect(self._answer_button_clicked)

        self.line_edit.resize(*self._config['line-edit']['size'])
        self.line_edit.setStyleSheet('QWidget { background-color: %s }' %
                                     self._config['line-edit']['background-color'])
        self.line_edit.move(*self._config['line-edit']['coordinates'])
        self.line_edit.setFont(QFont(*self._config['line-edit']['font']))

    def _configure_answer_button(self):
        self.answer_button.clicked.connect(self._answer_button_clicked)
        self.answer_button.setText('Start')
        self.answer_button.setToolTip('Push to count tonal')

        self.answer_button.setStyleSheet("""
                             QPushButton:hover { background-color: %s }
                             QPushButton:!hover { background-color: %s }
                             QPushButton:pressed { background-color: %s; }
                         """ % (self._config['answer-button']['background-color']['hover'],
                                self._config['answer-button']['background-color']['!hover'],
                                self._config['answer-button']['background-color']['pressed']))
        self.answer_button.resize(*self._config['answer-button']['size'])
        self.answer_button.move(*self._config['answer-button']['coordinates'])
        self.answer_button.setFont(QFont(*self._config['answer-button']['font']))

    def configure_voice_button(self):
        self.voice_button.setText('🎙')
        self.voice_button.setToolTip('Push to enter the text by speech')
        self.voice_button.clicked.connect(self._voice_button_clicked)

        self.voice_button.resize(*self._config['voice-button']['size'])
        self.voice_button.setFont(QFont(*self._config['voice-button']['font']))
        self.voice_button.move(*self._config['voice-button']['coordinates'])
        self.voice_button.setStyleSheet("""
                             QPushButton:hover { background-color: %s }
                             QPushButton:!hover { background-color: %s }
                             QPushButton:pressed { background-color: %s; }
                         """ % (self._config['voice-button']['background-color']['hover'],
                                self._config['voice-button']['background-color']['!hover'],
                                self._config['voice-button']['background-color']['pressed']))

    def _configure_delete_button(self):
        self.delete_button.setText('✗')
        self.delete_button.setToolTip('Push to clear text box')
        self.delete_button.clicked.connect(self._delete_button_clicked)

        self.delete_button.resize(*self._config['delete-button']['size'])
        self.delete_button.setFont(QFont(*self._config['delete-button']['font']))
        self.delete_button.move(*self._config['delete-button']['coordinates'])
        self.delete_button.setStyleSheet("""
                             QPushButton:hover { background-color: %s }
                             QPushButton:!hover { background-color: %s }
                             QPushButton:pressed { background-color: %s; }
                         """ % (self._config['delete-button']['background-color']['hover'],
                                self._config['delete-button']['background-color']['!hover'],
                                self._config['delete-button']['background-color']['pressed']))

    def _configure_file_dialog_button(self):
        self.file_dialog_button.setText('📂')
        self.file_dialog_button.setToolTip('Push to open file')
        self.file_dialog_button.clicked.connect(self._file_dialog_button_clicked)

        self.file_dialog_button.resize(*self._config['file-dialog-button']['size'])
        self.file_dialog_button.setFont(QFont(*self._config['file-dialog-button']['font']))
        self.file_dialog_button.move(*self._config['file-dialog-button']['coordinates'])
        self.file_dialog_button.setStyleSheet("""
                             QPushButton:hover { background-color: %s }
                             QPushButton:!hover { background-color: %s }
                             QPushButton:pressed { background-color: %s; }
                         """ % (self._config['file-dialog-button']['background-color']['hover'],
                                self._config['file-dialog-button']['background-color']['!hover'],
                                self._config['file-dialog-button']['background-color']['pressed']))

    def _configure_answer_label(self):
        self.answer_label.move(*self._config['answer-label']['coordinates'])
        self.answer_label.setFont(QFont(*self._config['answer-label']['font']))
        self.answer_label.resize(*self._config['answer-label']['size'])

    def launch(self):
        self.setWindowIcon(QIcon('icon.ico'))
        self.setWindowTitle('Sentiment Analyser')

        self._configure_main_window()
        self.show()

        self.__logger.info('Main window was successfully launched.', 'MainWindow.launch()')

    def _delete_button_clicked(self):
        self.line_edit.clear()
        self.answer_label.clear()

    def _voice_button_clicked(self):
        self.message_box.question(self, 'Speak', 'You can start speeking.', QMessageBox.Ok)

        voice_text = self._speech_recognizer.recognize_speech()

        if voice_text == 'Unknown value':
            try_again = QMessageBox.Yes

            while try_again == QMessageBox.Yes and voice_text == 'Unknown value':
                try_again = self.message_box.question(self, 'Error', 'Unknown value\n Try again?',
                                                      QMessageBox.Yes | QMessageBox.No)
                if try_again == QMessageBox.No:
                    break

                voice_text = self._speech_recognizer.recognize_speech()

        if voice_text == 'Internet connection lost':
            self.message_box.question(self, 'Error', 'Internet connection lost', QMessageBox.Ok)
            return None

        if voice_text == 'No microphone':
            self.message_box.question(self, 'Error', 'Microphone was disconnected', QMessageBox.Ok)
            return None

        if voice_text != 'Unknown value':
            self.line_edit.setText(voice_text)

            return None

    def _file_dialog_button_clicked(self):
        file_content = self._file_reader.get_file_content()
        if file_content:
            self.line_edit.setText(file_content)

    def _answer_button_clicked(self):
        self._text_tonal_analyzer.detect_tonal(self.line_edit.text())

        if self.os == 'windows':
            if self._text_tonal_analyzer.tonal == 'positive':
                self.answer_label.setStyleSheet('QLabel {color:rgba(0, 200, 100, 255)}')
                self.answer_label.move(193.5, 180)

            elif self._text_tonal_analyzer.tonal == 'negative':
                self.answer_label.setStyleSheet('QLabel {color:rgba(255, 56, 20, 255)}')
                self.answer_label.move(180, 180)

        elif self.os == 'darwin':
            if self._text_tonal_analyzer.tonal == 'positive':
                self.answer_label.setStyleSheet('QLabel {color:rgba(0, 200, 100, 255)}')
                self.answer_label.move(230, 210)

            elif self._text_tonal_analyzer.tonal == 'negative':
                self.answer_label.setStyleSheet('QLabel {color:rgba(255, 56, 20, 255)}')
                self.answer_label.move(225, 210)

        self.answer_label.setToolTip('Tonal and probability')

        if self._text_tonal_analyzer.probability:
            self.answer_label.setText(self._text_tonal_analyzer.tonal.capitalize() + '\n' +
                                      str(round(self._text_tonal_analyzer.probability * 100, 3)) + '%')
        else:
            self.answer_label.setText(self._text_tonal_analyzer.tonal.capitalize())


def read_mode():
    modes = ['console', 'gui']
    mode = input('mode: ')

    if mode not in modes:
        mode = 'console'

    return mode


def launch():
    mode = read_mode()

    if mode == 'gui':
        app = QApplication(sys.argv)

        main_window = MainWindow()
        main_window.launch()

        sys.exit(app.exec_())

    elif mode == 'console':
        print('Console mode. To exit enter 0.')

        text_tonal_analyzer = TextTonalAnalyzer()

        while True:
            text = input('\ntext: ')

            if text == '0':
                exit(0)

            text_tonal_analyzer.detect_tonal(text)
            tonal, probability = text_tonal_analyzer.tonal, text_tonal_analyzer.probability

            print('Tonal: %s' % tonal)
            print('Probability: %s\n' % str(probability))


launch()
