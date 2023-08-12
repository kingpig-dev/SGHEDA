from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox, QDialog


class Notification(QWidget):
    def __init__(self, message, notification_type, parent=None):
        super().__init__(parent)

        # Set window properties
        self.setWindowTitle("Notification")
        self.setWindowIcon(QIcon("./Images/logo03.png"))
        self.setFixedSize(300, 100)

        # Create message label and close button
        self.message_label = QLabel(message, self)
        self.close_button = QPushButton("x", self)

        # Set message label style based on notification type
        if notification_type == "error":
            self.message_label.setStyleSheet("color: red; font-weight: bold;")
        elif notification_type == "warning":
            self.message_label.setStyleSheet("color: orange; font-weight: bold;")

        # Create layout and add message label and close button
        layout = QVBoxLayout()
        layout.addWidget(self.message_label)
        layout.addWidget(self.close_button)
        self.setLayout(layout)

        # Connect close button to close method
        self.close_button.clicked.connect(self.close)

        # Show window and start timer to close it after 5 seconds
        self.show()
        self.timer = QTimer()
        self.timer.timeout.connect(self.close)
        self.timer.start(5000)

    def close(self):
        # Stop timer and close window
        self.timer.stop()

class CustomMessageBox(QDialog):
    def __init__(self, icon, title, text, parent=None):
        super().__init__(parent)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("""
            background-color: #374866;
            border-radius: 30px;
            border: 1px solid red;
            font-size: 16px;
            
        """)
        # Set window icon
        self.setWindowIcon(icon)

        # Create icon label
        icon_label = QLabel(self)
        icon_label.setPixmap(icon.pixmap(64, 64))
        icon_label.move(20,10)

        # Create text label
        text_label = QLabel(self)
        text_label.setText(text)
        text_label.setGeometry(100, 5, 200, 64)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.accept)
        self.timer.start(3000)

class ExitNotification(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
                background-color: #303E58;
                font-size: 20px;
                color: white;
                
                border-radius: 10px;
        """)

        self.setWindowTitle("Notification")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setText("Are you sure you want to exit?")
        self.setIcon(QMessageBox.Question)

        # Customize the buttons
        yes_button = self.addButton(QMessageBox.Yes)
        no_button = self.addButton(QMessageBox.No)

        # Apply custom styles to the buttons
        yes_button.setStyleSheet(
            """
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
            """
        )
        no_button.setStyleSheet(
            """
                QPushButton{
                    background-color: #333A51;
                    color: white;
                    border-radius: 10px;
                    padding: 3px 10px 3px 10px;
                    text-align: center;
                    text-decoration: none;
                    margin: 4px 2px;
                    border: 2px solid #C03647;
                    width: 80px;
                }
                QPushButton:hover {
                    background-color: #943A4C;
                }
            """
        )

        self.setDefaultButton(QMessageBox.No)

class Dialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(self.tr("Dialog"))
        self.setStyleSheet("""
            background-color: #1F2843;
            color: white;
        """)

        btn_alarm = QPushButton(self)
        btn_alarm.setText('alarm')
        btn_alarm.setGeometry(10, 200, 50, 30)
        btn_alarm.clicked.connect(self.alarm)

        btn_error = QPushButton(self)
        btn_error.setText('error')
        btn_error.setGeometry(60, 200, 50, 30)

        btn_warning = QPushButton(self)
        btn_warning.setText('warning')
        btn_warning.setGeometry(110, 200, 50, 30)

        self.resize(600, 300)

    def alarm(self):
        icon = QIcon('./Images/logo03.png')
        custom_message_box = CustomMessageBox(icon, 'Custom Message', 'This is a custom message.', self)
        custom_message_box.setGeometry(300, 20, 300, 70)
        custom_message_box.show()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = Dialog()
    w.show()
    sys.exit(app.exec_())