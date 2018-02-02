import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication, QPushButton


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.qle = QLineEdit(self)

        self.qle.resize(350, 30)
        self.qle.move(75, 40)

        self.btn = QPushButton("Ответ", self)
        self.btn.resize(120, 50)
        self.btn.move(190, 100)
        self.btn.clicked.connect(self.button_clicked)

        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle('Sentiment Analysis')
        self.show()

    def button_clicked(self):
        return self.qle.text()


def show_interface():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
