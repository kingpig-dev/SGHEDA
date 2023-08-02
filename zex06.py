import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 500, 500)

        # Create a QTextEdit widget to display the file contents
        self.textEdit = QTextEdit(self)
        self.setCentralWidget(self.textEdit)

        # Create a QAction to open a file
        openFile = QAction('Open', self)
        openFile.triggered.connect(self.showDialog)

        # Create a menu bar and add the openFile QAction to it
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')
        fileMenu.addAction(openFile)

    def showDialog(self):
        # Show a file dialog to select a JSON file
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'JSON files (*.json)')

        if fileName:
            # Load the JSON data from the file
            with open(fileName, 'r') as f:
                data = json.load(f)

            # Display the JSON data in the QTextEdit widget
            self.textEdit.setText(json.dumps(data, indent=4))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())