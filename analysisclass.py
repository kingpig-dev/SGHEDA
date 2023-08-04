import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMainWindow, QTabWidget, \
    QHBoxLayout, QSizePolicy, QComboBox
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtCore import Qt

from buttonclass import ImageButton, ExtraButton, SquareButton, ExitButton


class AnalysisClass(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # set the size of window
        self.setFixedSize(1210, 790)

        # Set the background color of the main window
        self.setStyleSheet("background-color: #1F2843; border: none")

        # add all widgets

        self.left_widget = QWidget()
        self.left_widget.setStyleSheet('background-color: #2C3751;')

        # Image button
        self.btn_home = ImageButton(self.left_widget, './Images/logo03.png')
        self.btn_home.move(20, 20)
        self.btn_home.clicked.connect(self.parent.dashboardUI)

        self.combobox_selection = QComboBox(self.left_widget)
        self.icon_design = QIcon('./Images/design01.png')
        self.icon_analysis = QIcon('./Images/analysis02.png')
        self.combobox_selection.addItem(self.icon_design, '  Design ')
        self.combobox_selection.addItem(self.icon_analysis, ' Analysis ')
        self.combobox_selection.resize(110, 30)
        self.combobox_selection.setCursor(QCursor(Qt.PointingHandCursor))
        self.combobox_selection.setStyleSheet("""            
             QComboBox {
                color: #7C8AA7;
                background-color: #2C3751;
                selection-background-color: #555555;
                padding: 1px 18px 1px 3px;
                min-width: 6em;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                width: 15px;

                border: none;
            }
        """)
        self.combobox_selection.move(10, 150)

        self.label_num = QLabel(self.left_widget)
        self.label_num_icon = QPixmap('./Images/remain01.png')
        self.label_num.setPixmap(self.label_num_icon.scaled(25, 25))
        self.label_num.setText(' 5')
        self.label_num.setGeometry(130, 150, 140, 30)
        self.label_num.setStyleSheet("""
            QLabel {
                background-color: #2C3751;
                color: #7C8AA7;
                font-size: 16px;
            }
            QLabel hover {
                background-color: #5A6B90;
            }
        """)

        self.btn_1 = SquareButton(self.left_widget, './Images/fluid02.png')
        self.btn_1.setText(' Fluid')
        self.btn_1.setGeometry(0, 200, 200, 50)
        self.btn_2 = SquareButton(self.left_widget, './Images/soil01.png')
        self.btn_2.setText(' Soil')
        self.btn_2.setGeometry(0, 250, 200, 50)
        self.btn_3 = SquareButton(self.left_widget, './Images/pipe01.png')
        self.btn_3.setText(' Piping')
        self.btn_3.setGeometry(0, 300, 200, 50)
        self.btn_4 = SquareButton(self.left_widget, './Images/configuration01.png')
        self.btn_4.setText(' Configuration')
        self.btn_4.setGeometry(0, 350, 200, 50)
        self.btn_5 = SquareButton(self.left_widget, './Images/power02.png')
        self.btn_5.setText(' Extra Kw')
        self.btn_5.setGeometry(0, 400, 200, 50)

        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)

        self.btn_setting = ExtraButton(self.left_widget, './Images/setting02.png')
        self.btn_setting.setText(' Setting')
        self.btn_setting.setGeometry(0, 550, 200, 50)

        self.btn_license = ExtraButton(self.left_widget, './Images/license01.png')
        self.btn_license.setText(' License')
        self.btn_license.setGeometry(0, 600, 200, 50)

        self.btn_help = ExtraButton(self.left_widget, './Images/help.png')
        self.btn_help.setText('  Help  ')
        self.btn_help.setGeometry(0, 650, 200, 50)

        self.btn_exit = ExitButton(self.left_widget)
        self.btn_exit.setText(' Exit')
        self.btn_exit.setGeometry(0, 700, 200, 50)

        # add tabs
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()

        # right widget
        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')

        self.right_widget.setCurrentIndex(0)
        self.right_widget.setStyleSheet('''
            QTabWidget {
                border: none;
            }

            QTabBar::tab{
                width: 0;
                height: 0; 
                margin: 0; 
                padding: 0; 
                border: none;
            }
        ''')

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 20)
        main_layout.setStretch(1, 100)
        self.setLayout(main_layout)

    # -----------------
    # buttons

    def button1(self):
        self.right_widget.setCurrentIndex(0)

    def button2(self):
        self.right_widget.setCurrentIndex(1)

    def button3(self):
        self.right_widget.setCurrentIndex(2)

    def button4(self):
        self.right_widget.setCurrentIndex(3)
        # self.parent.dashboardUI()

    # -----------------
    # pages

    def ui1(self):
        main = QWidget()

        return main

    def ui2(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 2'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui3(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 3'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui4(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 4'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AnalysisClass()
    ex.show()
    sys.exit(app.exec_())