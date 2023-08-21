import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QApplication, QWidget, QHBoxLayout, \
    QMainWindow, QGroupBox, QComboBox
from labelclass import IntroLabel3, ImageButton
from cryptography.fernet import Fernet
import pyperclip
class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # self.setFixedHeight(100)
        self.resize(parent.width(), 23)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Title label
        self.title_label = QLabel("  SGHEDA (Slinky GHE Design & Analysis)")
        layout.addWidget(self.title_label)

        # Minimize button
        self.minimize_button = QPushButton("—")
        self.minimize_button.setFixedSize(34, 23)
        self.minimize_button.setStyleSheet('''
            QPushButton {
                border: none;
            }
            QPushButton:hover {
                background-color: #E5E5E5;
                color: white;
            }
        ''')
        self.minimize_button.clicked.connect(parent.showMinimized)
        layout.addWidget(self.minimize_button)

        # Close button
        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(34, 23)
        self.close_button.setStyleSheet('''
            QPushButton {
                border: none;
            }
            QPushButton:hover {
                background-color: #E81123;
                color: white;
            }
        ''')
        self.close_button.clicked.connect(parent.close)
        layout.addWidget(self.close_button)

        # Set stylesheet for custom title bar
        self.setStyleSheet("""
            background-color: #F1F1F1;
            color: #ABABAB;
            font-weight: bold;
            font-size: 10px;
            text-align: center;
        """)

        # Set the title bar widget as the window's title bar
        self.parent().setWindowFlags(Qt.FramelessWindowHint)
        # self.parent().setWindowTitle("Custom Title Bar")
        # self.parent().layout().setContentsMargins(0, self.height(), 0, 0)
        self.parent().layout().addWidget(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent().drag_position = event.globalPos() - self.parent().frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent().move(event.globalPos() - self.parent().drag_position)
            event.accept()


class Myapp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet('''
            background-color: #1F2843;
            color: white;
            border: none;
            font-size: 16px;
        ''')
        self.encryption_key = 5
        self.state = 0

        self.resize(610, 250)

        self.btn_home = ImageButton(self, './Images/logo03_glowed_white.png')
        self.btn_home.resize(165, 140)
        self.btn_home.move(0, 60)

        self.label_title = IntroLabel3(self)
        self.label_title.setText('License Information')
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setGeometry(250, 35, 200, 30)

        self.label_machinenumber = QLabel(self)
        self.label_machinenumber.setText("Machine Number")
        self.label_machinenumber.setStyleSheet('''
                            QLabel {
                                text-align: center;
                            }
                        ''')

        self.machinenumber = QLineEdit(self)
        self.machinenumber.setAlignment(Qt.AlignCenter)
        self.machinenumber.setStyleSheet('''
                                    QLineEdit {
                                        text-align: center;
                                        background-color: #1F2843;
                                        border: none;
                                        border-bottom: 2px solid #1F8EFA;
                                    }
                                ''')
        self.label_machinenumber.setGeometry(180, 65, 130, 40)
        self.machinenumber.setGeometry(320, 70, 270, 30)

        self.groupbox = QGroupBox(self)
        self.groupbox.setTitle('License Type')

        self.combobox_selection = QComboBox(self.left_widget)
        self.icon_design = QIcon('./Images/design.png')
        self.icon_analysis = QIcon('./Images/analysis02.png')
        self.combobox_selection.addItem(self.icon_design, ' Design')
        self.combobox_selection.addItem(self.icon_analysis, 'Analysis ')
        self.combobox_selection.resize(100, 30)
        self.combobox_selection.setCursor(QCursor(Qt.PointingHandCursor))
        self.combobox_selection.setStyleSheet(""" 
                     QComboBox {
                        color: #7C8AA7;
                        background-color: #2C3751;
                        selection-background-color: white;
                        padding: 1px 1px 1px 1px;
                        min-width: 2em;
                        font-size: 16px;
                    }

                    QComboBox:hover {
                        color: #2978FA;
                    }

                    QComboBox::drop-down {
                        subcontrol-origin: padding;
                        color: white;
                        width: 10px;
                        border: none;
                    }

                    QComboBox::down-arrow {
                        border: 0px;
                        background-image-width: 30px;
                        border-image: url(./Images/down.png);
                    }
                """
                                              )
        self.combobox_selection.currentIndexChanged.connect(self.combobox_selection_changed)
        self.combobox_selection.move(20, 155)


        self.label_serialnumber = QLabel(self)
        self.label_serialnumber.setText('Serial Number')
        self.label_serialnumber.setStyleSheet('''
                                   QLabel {
                                       text-align: center;
                                   }
                               ''')
        self.serialnumber = QLineEdit(self)
        self.serialnumber.setAlignment(Qt.AlignCenter)
        self.serialnumber.setStyleSheet('''
                                   QLineEdit {
                                       text-align: center;
                                       background-color: #1F2843;
                                       border: none;
                                       border-bottom: 2px solid #1F8EFA;
                                   }
                               ''')
        self.label_serialnumber.setGeometry(180, 160, 130, 30)
        self.serialnumber.setGeometry(320, 160, 270, 30)
        self.serialnumber.setReadOnly(True)
        # self.serialnumber.mousePressEvent()

        self.btn_confirm = QPushButton(self)
        self.btn_confirm.setText('Generate')
        self.btn_confirm.setStyleSheet("""
                        QPushButton{
                            background-color: #333A51;
                            color: white;
                            border-radius: 10px;
                            padding: 3px 10px 3px 10px;
                            text-align: center;
                            text-decoration: none;
                            margin: 4px 2px;
                            border: 2px solid #6B963B;
                            width: 80px;
                        }
                        QPushButton:hover {
                            background-color: #5D7C4C;
                        }
                    """)
        self.btn_confirm.setGeometry(280, 200, 130, 40)
        self.btn_confirm.clicked.connect(self.generate_license)

    def generate_license(self):
        print("generate license")
        machine_number = self.machinenumber.text()
        if machine_number:
            print("machine number: ", machine_number)

            # get use number
            num_design = '{:4d}'.format(45).replace(' ', '0')
            num_analysis = '{:4d}'.format(45).replace(' ', '0')
            data = num_design + machine_number[8:16] + num_analysis + machine_number[0:8]

            # encrypt data with key
            self.encrypted_data = self.caesar_encrypt(data, self.encryption_key)
            self.serialnumber.setText(self.encrypted_data)
            self.state = 1

            # decrypt data with key
            self.decrypted_data = self.caesar_decrypt(self.encrypted_data, self.encryption_key)

    def caesar_encrypt(self, plaintext, shift):
        ciphertext = ""
        for char in plaintext:
            # Encrypt uppercase letters
            if char.isupper():
                encrypted_char = chr((ord(char) - 65 + shift) % 26 + 65)
            # Encrypt lowercase letters
            elif char.islower():
                encrypted_char = chr((ord(char) - 97 + shift) % 26 + 97)
            # digit
            elif char.isdigit():
                encrypted_char = chr((ord(char) - 48 + shift) % 10 + 48)
            else:
                # Leave non-alphabetic characters unchanged
                encrypted_char = char
            ciphertext += encrypted_char
        print("ciphertext", ciphertext)
        return ciphertext

    def caesar_decrypt(self, ciphertext, shift):
        plaintext = ""
        for char in ciphertext:
            # Decrypt uppercase letters
            if char.isupper():
                decrypted_char = chr((ord(char) - 65 - shift) % 26 + 65)
            # Decrypt lowercase letters
            elif char.islower():
                decrypted_char = chr((ord(char) - 97 - shift) % 26 + 97)
            # Decrypt digit
            elif char.isdigit():
                decrypted_char = chr((ord(char) - 48 - shift) % 10 + 48)
            else:
                # Leave non-alphabetic characters unchanged
                decrypted_char = char
            plaintext += decrypted_char
        print("plaintext: ", plaintext)
        return plaintext
    def copy_clipboard(self):
        print('copy clipboardd')

if __name__ == "__main__":

    app = QApplication(sys.argv)
    my_app = Myapp()
    titlebar = CustomTitleBar(my_app)
    my_app.show()
    sys.exit(app.exec_())