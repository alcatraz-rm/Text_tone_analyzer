# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


import sys
import time
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication, QPushButton, QComboBox, QMessageBox
from modules.count_text_tonal.count_text_tonal import count_text_tonal
from PyQt5.QtGui import QFont, QIcon


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('icon.ico'))
        self.qle = QLineEdit(self)
        self.qle.resize(350, 30)
        self.qle.move(75, 40)
        self.qle.setFont(QFont("Times", 14))

        self.lbl = QLabel(self)
        self.lbl.move(50, 150)
        self.lbl.setFont(QFont("Times", 14))
        self.lbl.resize(300, 100)

        self.btn = QPushButton("Посчитать тональность", self)
        self.btn.resize(180, 50)
        self.btn.move(150, 100)
        self.btn.clicked.connect(self.button_clicked)
        # self.btn.show()

        self.setGeometry(500, 500, 500, 300)
        self.setWindowTitle('Sentiment Analyser')
        self.show()

    def button_clicked(self):
        tonal, weight = count_text_tonal(self.qle.text())
        self.lbl.setText('Text Tonal: ' + tonal + '\n' + 'Text Weight: ' + str(weight))


class SysInfGet(QWidget):
    def __init__(self):
        self.input_method = ''
        self.output_method = ''
        super().__init__()
        self.initUI()

    def get_input_text(self, text):
        self.input_method = text

    def get_output_text(self, text):
        self.output_method = text

    def ok_button_clicked(self):
        if (self.output_method == 'File' or self.output_method == 'Screen') and (self.input_method == 'Manually' or
                                                        self.input_method == 'File' or self.input_method == 'Voice'):
            with open('sys_inf.txt', 'w') as file:
                file.write(self.input_method + ';' + self.output_method)
                self.close()
        else:
            self.err_label.setText('All fields must be fill in')
            self.err_label.show()

    def initUI(self):
        self.setWindowTitle('Sentiment Analyser')
        self.setWindowIcon(QIcon('icon.ico'))
        self.setGeometry(250, 250, 300, 250)

        # init a block to select an input method
        self.input_method_combo = QComboBox(self)
        self.input_method_combo.addItems(['...', 'Manually', 'Voice', 'File'])
        self.input_method_combo.move(200, 50)
        self.input_method_combo.setFont(QFont("Times", 12))

        self.label1 = QLabel(self)
        self.label1.setFont(QFont("Times", 12))
        self.label1.setText('Select the input method:')
        self.label1.move(10, 55)

        # init a block to select output method
        self.output_method_combo = QComboBox(self)
        self.output_method_combo.addItems(['...', 'Screen', 'File'])
        self.output_method_combo.move(200, 100)
        self.output_method_combo.setFont(QFont("Times", 12))

        self.label2 = QLabel(self)
        self.label2.setFont(QFont("Times", 12))
        self.label2.setText('Select the output method:')
        self.label2.move(10, 105)

        # init error label
        self.err_label = QLabel(self)
        self.err_label.setFont(QFont("Times", 11))
        self.err_label.setStyleSheet("QLabel {color:rgba(255, 99, 71, 255)}")
        self.err_label.resize(150, 30)
        self.err_label.move(90, 10)

        # init "OK" button
        self.ok_button = QPushButton("OK", self)
        self.ok_button.resize(150, 50)
        self.ok_button.move(75, 155)
        self.ok_button.clicked.connect(self.ok_button_clicked)

        self.show()
        self.input_method_combo.activated[str].connect(self.get_input_text)
        self.output_method_combo.activated[str].connect(self.get_output_text)


app = QApplication(sys.argv)
sys_inf_get = SysInfGet()
sys.exit(app.exec_())
