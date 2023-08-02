import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class InputForm(QWidget):

    def __init__(self, parent, elements):
        super().__init__(parent)

        self.setStyleSheet('''
            background-color: #1F2843;
            color: white;
            border: 1px solid red;
            font-size: 16px;
        ''')
        self.setWindowTitle(elements[0])
        self.layout = QVBoxLayout(self)
        self.input = []
        for i in range(1, len(elements)):
            a = QLabel(elements[i][0])

            b = QLineEdit()
            b.setMaxLength(4)
            b.setStyleSheet('''
                background-color: #1F2843;
                border: none;
            ''')

            c = QLabel(elements[i][1])
            d = QHBoxLayout()
            d.addWidget(a)
            d.addWidget(b)
            d.addWidget(c)

            self.layout.addLayout(d)
            self.input.append(b)

        self.btn_next = QPushButton()
        self.btn_next.setText("Next")
        self.btn_next.clicked.connect(self.btnnext)
        self.layout.addWidget(self.btn_next)
        self.setLayout(self.layout)


    def btnnext(self):
        for a in self.input:
            print(a.text())

    def textchanged(self, text):
        print("contents of text box: " + text)


    def enterPress(self):
        print("edited")

class Dialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(self.tr("Dialog"))

        b = ["System Design", ["Inlet Temperature", "dF"], ["Flow Rate", "gpm/ton"]]
        a = InputForm(self, b)

        self.resize(400, 300)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = Dialog()
    w.show()
    sys.exit(app.exec_())
