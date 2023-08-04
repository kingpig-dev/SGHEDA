from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget

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
        self.hide()


class Dialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(self.tr("Dialog"))

        window = Notification("This is a test notification", "message", self)
        window.move(app.desktop().screen().rect().topRight() - window.rect().topRight())

        self.resize(600, 300)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = Dialog()
    w.show()
    sys.exit(app.exec_())