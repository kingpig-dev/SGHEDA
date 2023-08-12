import sys
from PyQt5.QtCore import Qt

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from labelclass import IntroLabel3

import traceback
class InputForm(QWidget):

    def __init__(self, parent, elements):
        super().__init__(parent)
        self.setStyleSheet('''
            background-color: #1F2843;
            color: white;
            font-size: 16px;
            padding: 5px 10px;
            QWidget {
                border: 2px solid red;
            }
            
        ''')
        self.elements = elements
        self.grid = QGridLayout(self)
        label_title = IntroLabel3(elements[0])
        label_title.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(label_title, 1, 0, 1, 3)
        self.input = []
        for i in range(1, len(elements)):
            if elements[i][2] == 'lineedit':
                a = QLabel(elements[i][0])
                a.setStyleSheet('''
                    QLabel {
                        text-align: center;
                    }
                ''')
                b = QLineEdit()
                b.setValidator(QDoubleValidator())
                b.setMaxLength(10)
                b.setStyleSheet('''
                    QLineEdit {
                        text-align: center;
                        background-color: #1F2843;
                        border: none;
                        border-bottom: 2px solid #1F8EFA;
                    }
                ''')
                b.setText(elements[i][3])
                b.setAlignment(Qt.AlignCenter)
                c = QLabel(elements[i][1])
                self.grid.addWidget(a, i + 1, 0)
                self.grid.addWidget(b, i + 1, 1)
                self.grid.addWidget(c, i + 1, 2)

                self.input.append(b)

            elif elements[i][2] == 'combobox':

                a = QLabel(elements[i][0])

                b = QComboBox()
                b.addItems(elements[i][1])
                b.setStyleSheet("""            
                     QComboBox {
                        background-color: #2C3751;
                        selection-background-color: #555555;
                        min-width: 2em;
                        font-size: 16px;
                        text-align: center;
                    }
                    
                    QComboBox::hover{
                        color: #2978FA
                    }
                    
                    QComboBox::drop-down {
                        subcontrol-origin: padding;
                        width: 7px;
                        border: none;
                    }
                    
                    QComboBox::down-arrow {
                        border: 0px;
                        background-image-width: 30px;
                        border-image: url(./Images/down.png);
                    }
                """
                )

                self.grid.addWidget(a, i + 1, 0)
                self.grid.addWidget(b, i + 1, 1, 1, 2)
                self.input.append(b)

        # self.btn_next = QPushButton()
        # self.btn_next.setText("Next")
        # self.btn_next.clicked.connect(self.btnnext)
        # self.grid.addWidget(self.btn_next, 5, 1)
        self.grid.setAlignment(Qt.AlignCenter)
        self.setLayout(self.grid)

    def btnnext(self):
        if self.getValidation():
            self.getData()

    def getData(self):
        dict = {}
        for i in range(1, len(self.input) + 1):
            # print(self.elements[i][2], i)
            if self.elements[i][2] == "lineedit":
                dict[self.elements[i][0]] = self.input[i - 1].text()
                print(self.input[i - 1].text())
            elif self.elements[i][2] == "combobox":
                dict[self.elements[i][0]] = self.input[i - 1].currentText()
                print(self.input[i - 1].currentText())
        return dict

    def getValidation(self):
        for i in range(1, len(self.input) + 1):
            if self.elements[i][2] == "lineedit":
                if self.input[i - 1].text() == "":
                    return False
        return True

    def setData(self, data):
        print('setData')
        try:
            for i in range(1, len(self.input) + 1):
                if self.elements[i][2] == "lineedit":
                    self.input[i - 1].setText(data[i][3])
                else:
                    self.input[i - 1].setText(data[i][2])
        except Exception as e:
            print('setData expeption: ', traceback.format_exc())

    def setReadOnly(self, data):
        for i in range(1, len(self.input)+1):
            self.input[i-1].setReadOnly(data)

class InputDescription(QWidget):
    def __init__(self, parent, elements):
        super().__init__(parent)
        self.setStyleSheet('''
            background-color: #1F2843;
            color: white;
            font-size: 16px;
            padding: 5px 10px;
            QWidget {
                border: 2px solid red;
            }

        ''')
        self.elements = elements
        self.grid = QGridLayout(self)
        label_title = IntroLabel3(elements[0])
        label_title.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(label_title, 1, 0, 1, 3)

        self.description = CustomQTextEdit(self)
        self.description.setText(elements[1])
        self.grid.addWidget(self.description, 2, 0, 3, 3)
    def getData(self):
        return self.description.toPlainText()

    def getValidation(self):
        if self.description.toPlainText() == '':
            return False
        else:
            return True
class CustomQTextEdit(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("""
            background-color: #2C3751;
            color: #7C8AA7;
            font-size: 16px;
            padding: 4px 3px 4px 2px;
        """)



class Dialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            background-color: #1F2843;
        """)
        self.setWindowTitle(self.tr("Dialog"))

        b = ["System Design", ["Inlet Temperature", "dF", "lineedit", '90'],
             ["Flow Rate", "gpm/ton", "lineedit", '3.0'], ["Fluid type", ["Water", "Methanol"], "combobox"]]
        a = InputForm(self, b)

        c = CustomQTextEdit(self)
        c.setText("Initial")
        print(c.toPlainText())
        self.resize(600, 300)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = Dialog()
    w.show()
    sys.exit(app.exec_())
