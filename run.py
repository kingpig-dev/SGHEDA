import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
import sqlite3

from dashboardclass import Dashboard
from designclass import DesignClass

class Myapp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1210, 790)
        self.setStyleSheet("background-color: #1F2843;")

        # Set the window title
        self.setWindowTitle('Slinky GHE Design & Analysis')
        self.setWindowIcon(QIcon("./Images/logo03.png"))

        # Create a layout for the central widget

        self.design = DesignClass(self)
        self.design.move(1000, 1000)

        self.dashboard = Dashboard(self)

    def designUI(self):
        print("designUI")
        self.dashboard.move(1000, 1000)
        self.design.move(0, 0)
        self.design.right_widget.setCurrentIndex(0)

    def dashboardUI(self):
        print("dashboardUI")
        self.design.move(1000, 1000)
        self.dashboard.move(0, 0)

if __name__ == '__main__':
    # Create a new QApplication instance
    app = QApplication(sys.argv)

    # Create a new MyApp instance
    my_app = Myapp()

    # Show the main window
    my_app.show()

    # Start the event loop
    sys.exit(app.exec_())
