import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QApplication, QWidget, QHBoxLayout, \
    QMainWindow
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
        self.encryption_key = b'-EDDWkBVgJ_O-dKDDlxbkMCgf322qlW_lYUj2JI2ExU='
        self.state = 0

        self.resize(610, 250)

        self.btn_home = ImageButton(self, './Images/logo03_glowed_white.png')
        self.btn_home.resize(165, 140)
        self.btn_home.move(0, 60)

        self.label_title = IntroLabel3(self)
        self.label_title.setText('License Information')
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setGeometry(250, 50, 200, 30)

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
        self.label_machinenumber.setGeometry(180, 85, 130, 40)
        self.machinenumber.setGeometry(320, 90, 270, 30)

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
                                       font-size: 14px;
                                   }
                               ''')
        self.label_serialnumber.setGeometry(180, 130, 130, 30)
        self.serialnumber.setGeometry(320, 130, 270, 30)
        self.serialnumber.setReadOnly(True)
        self.serialnumber.mousePressEvent()

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
        self.btn_confirm.setGeometry(280, 180, 130, 40)
        self.btn_confirm.clicked.connect(self.generate_license)

    def generate_license(self):
        print("generate license")
        machine_number = self.machinenumber.text()
        if machine_number:
            print("machine number: ", machine_number)

            # get use number
            num_design = str(0)
            num_analysis = str(0)
            data = machine_number + num_design + num_analysis

            # encrypt data with key
            cipher_suite = Fernet(self.encryption_key)
            self.encrypted_data = cipher_suite.encrypt(data.encode())

            self.serialnumber.setText(self.encrypted_data.decode())
            self.state = 1

    def copy_clipboard(self):
        print('copy clipboardd')

if __name__ == "__main__":

    app = QApplication(sys.argv)
    my_app = Myapp()
    titlebar = CustomTitleBar(my_app)
    my_app.show()
    sys.exit(app.exec_())