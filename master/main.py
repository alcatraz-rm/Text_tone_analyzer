# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication, QPushButton
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

        self.setGeometry(500, 500, 500, 300)
        self.setWindowTitle('Sentiment Analyser')
        self.show()

    def button_clicked(self):
        tonal, weight = count_text_tonal(self.qle.text())
        self.lbl.setText('Text Tonal: ' + tonal + '\n' + 'Text Weight: ' + str(weight))


app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())
