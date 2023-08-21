import json
import sys
import threading
import time
import webbrowser
import traceback

# UI
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTabWidget, \
    QHBoxLayout, QComboBox, QFileDialog, QScrollArea, QMessageBox
from PyQt5.QtGui import QIcon, QCursor, QMovie
from PyQt5.QtCore import Qt, QSize, QTimer, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Self define
from buttonclass import ImageButton, ExtraButton, SquareButton, ExitButton, MainButton1, ImageButton1, TextButton
from firstpageclass import FirstPageClass
from inputformclass import InputForm, CustomQTextEdit, LicenseForm, PersonalForm
from labelclass import IntroLabel1, TickerLabel, IntroLabel3
from notificationclass import CustomMessageBox, ExitNotification
import pyqtgraph as pg

# Calculation
import numpy as np
from scipy.special import erfc
import math

# license
import hashlib
import uuid
import sqlite3

class DesignClass(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.num_design = 0
        self.num_analysis = 0
        self.program_version = "1.0"

        # Get data
        self.database_connection = sqlite3.connect("./Logs/log/bin/data.db")
        self.database_cursor = self.database_connection.cursor()
        self.database_get_data()

        self.tabstack = []
        self.dict = {}
        self.designpath = './Logs/designpath.json'
        self.currentgldpath = ''

        # UI
        self.license_info = None
        self.plt_gfunction = None
        # calculation
        self.analysis_calculation_result = False
        self.analysis_calculation_process = False

        # set the size of window
        self.setFixedSize(1210, 770)

        # Set the background color of the main window
        self.setStyleSheet("background-color: #1F2843; border: none")
        # self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        # self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

        # add all widgets
        self.left_widget = QWidget()
        self.left_widget.setStyleSheet("""
            background-color: #2C3751;
            border-radius: 10px;
        """)

        # Image button
        self.btn_home = ImageButton(self.left_widget, './Images/logo03_glowed_white.png')
        self.btn_home.move(20, 20)
        self.btn_home.clicked.connect(self.button0)

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

        self.label_num = QPushButton(self.left_widget)
        self.label_num_icon = QIcon('./Images/remain01.png')
        self.label_num.setIcon(self.label_num_icon)
        self.label_num.setIconSize(QSize(25, 25))
        self.label_num.setText(' ' + str(self.num_design))
        self.label_num.setGeometry(130, 155, 80, 30)
        self.label_num.setStyleSheet("""
            QPushButton {
                background-color: #374866;
                color: white;
                font-size: 16px;
                border-radius: 13px;
                transition: background-color 0.9s ease-in-out;
            }
            QPushButton:hover {
                background-color: #5A6B90;
            }
        """)
        self.label_num.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.btn_1 = SquareButton(self.left_widget, './Images/configuration01_b.png', './Images/configuration01.png')
        self.btn_1.setText(' System Design ')
        self.btn_1.setGeometry(0, 200, 212, 50)
        self.btn_2 = SquareButton(self.left_widget, './Images/fluid02_b.png', './Images/fluid02.png')
        self.btn_2.setText(' Fluid Properties ')
        self.btn_2.setGeometry(0, 250, 212, 50)
        self.btn_3 = SquareButton(self.left_widget, './Images/soil01_b.png', './Images/soil01.png')
        self.btn_3.setText(' Soil Properties ')
        self.btn_3.setGeometry(0, 300, 212, 50)
        self.btn_4 = SquareButton(self.left_widget, './Images/pipe01_b.png', './Images/pipe01.png')
        self.btn_4.setText(' Pipe Design')
        self.btn_4.setGeometry(0, 350, 212, 50)
        self.btn_5 = SquareButton(self.left_widget, './Images/power02_b.png', './Images/power02.png')
        self.btn_5.setText(' Pump Info ')
        self.btn_5.setGeometry(0, 400, 212, 50)
        self.btn_6 = SquareButton(self.left_widget, './Images/result01_b.png', './Images/result01.png')
        self.btn_6.setText(' Design Result')
        self.btn_6.setGeometry(0, 450, 212, 50)
        self.btn_7 = SquareButton(self.left_widget, './Images/analysis11_b.png', './Images/analysis11.png')
        self.btn_7.setText(' Analysis')
        self.btn_7.setGeometry(0, 500, 212, 50)

        self.btn_1_ticker = TickerLabel(self.left_widget)
        self.btn_1_ticker.setGeometry(180, 210, 30, 30)
        self.btn_1_ticker.hide()

        self.btn_2_ticker = TickerLabel(self.left_widget)
        self.btn_2_ticker.setGeometry(180, 260, 30, 30)
        self.btn_2_ticker.hide()

        self.btn_3_ticker = TickerLabel(self.left_widget)
        self.btn_3_ticker.setGeometry(180, 310, 30, 30)
        self.btn_3_ticker.hide()

        self.btn_4_ticker = TickerLabel(self.left_widget)
        self.btn_4_ticker.setGeometry(180, 360, 30, 30)
        self.btn_4_ticker.hide()

        self.btn_5_ticker = TickerLabel(self.left_widget)
        self.btn_5_ticker.setGeometry(180, 410, 30, 30)
        self.btn_5_ticker.hide()

        self.btn_6_ticker = TickerLabel(self.left_widget)
        self.btn_6_ticker.setGeometry(180, 460, 30, 30)
        self.btn_6_ticker.hide()

        self.btn_7_ticker = TickerLabel(self.left_widget)
        self.btn_7_ticker.setGeometry(180, 510, 30, 30)
        self.btn_7_ticker.hide()

        self.slide_label = QLabel(self.left_widget)
        self.slide_label.setStyleSheet('background-color: #31A8FC')
        self.slide_label.resize(5, 50)
        self.slide_label.hide()

        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)
        self.btn_5.clicked.connect(self.button5)
        self.btn_6.clicked.connect(self.button6)
        self.btn_7.clicked.connect(self.button7)

        self.btn_setting = ExtraButton(self.left_widget, './Images/setting_b.png', './Images/setting.png')
        self.btn_setting.setText(' Settings')
        self.btn_setting.setGeometry(0, 590, 200, 50)
        self.btn_setting.clicked.connect(self.btnsetting)

        self.line = QLabel(self.left_widget)
        self.line.setStyleSheet('''
            QLabel {background-color: #ACACBF;;}
        ''')
        self.line.setGeometry(25, 640, 150, 1)


        self.btn_feedback = TextButton(self.left_widget)
        self.btn_feedback.setText(' Feedback')
        self.btn_feedback.clicked.connect(self.redirect_to_feedback)
        self.btn_feedback.setGeometry(50, 650, 100, 20)

        self.btn_help = TextButton(self.left_widget)
        self.btn_help.setText('  Help  ')
        self.btn_help.clicked.connect(self.redirect_to_help)
        self.btn_help.setGeometry(50, 675, 100, 20)


        self.btn_exit = ExitButton(self.left_widget, './Images/end01.png', './Images/end01_r.png')
        self.btn_exit.setText(' Exit')
        self.btn_exit.setGeometry(0, 695, 200, 50)
        self.btn_exit.clicked.connect(self.btnexit)

        # add tabs
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()
        self.tab5 = self.ui5()
        self.tab6 = self.ui6()
        self.tab7 = self.ui7()
        self.tab8 = self.ui8()
        self.tab9 = self.ui9()

        # right widget
        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')
        self.right_widget.addTab(self.tab5, '')
        self.right_widget.addTab(self.tab6, '')
        self.right_widget.addTab(self.tab7, '')
        self.right_widget.addTab(self.tab8, '')
        self.right_widget.addTab(self.tab9, '')

        # self.tab1.loadtable()
        self.right_widget.setCurrentIndex(0)

        self.right_widget.setStyleSheet('''
            QTabWidget::pane {
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
        main_layout.setStretch(0, 22)
        main_layout.setStretch(1, 100)
        self.setLayout(main_layout)

    def database_get_data(self):
        try:
            # get data from db
            self.database_cursor.execute("SELECT * FROM property")
            rows = self.database_cursor.fetchall()
            print("rows: ", len(rows))

            # set data if data not exist
            if len(rows) > 0:
                json_data = json.loads(rows[-1][1])

                # set class property
                self.num_design = json_data["Design"]
                self.num_analysis = json_data["Analysis"]
                print('loaddata')
            elif len(rows) == 0:
                self.database_set_data()

        except Exception as e:
            print('getdata Exception: ', e)
            # create db file if no exist
            self.database_cursor.execute('''CREATE TABLE IF NOT EXISTS property
                              (id INTEGER PRIMARY KEY, data TEXT)''')
            self.database_connection.commit()
            self.database_set_data()

    def database_set_data(self):
        json_data = {
            'Design': self.num_design,
            'Analysis': self.num_analysis
        }
        self.database_cursor.execute("insert into property (data) values (?)", (json.dumps(json_data),))
        self.database_connection.commit()
        print("Completely store data")

    def get_machine_number(self):
        # Get operating system version
        mac_address = uuid.getnode()

        # Combine OS version and program version
        combined_str = f"{mac_address}-{self.program_version}"

        # Generate a hash of the combined string
        hash_value = hashlib.md5(combined_str.encode()).hexdigest()
        machine_number = hash_value[:16]
        return machine_number

    def tickerbutton(self):
        currentIndex = self.right_widget.currentIndex()
        # print('currentIndex: ', currentIndex)
        if self.right_widget.currentIndex() == 0:
            self.slide_label.hide()
        else:
            self.slide_label.move(0, 200 + 50 * (currentIndex - 1))
            self.slide_label.show()

    # combobox
    def combobox_selection_changed(self):
        selected_text = self.combobox_selection.currentText()
        print(selected_text)
        if selected_text == ' Design':
            self.label_num.setText(' ' + str(self.num_design))
        else:
            self.label_num.setText(' ' + str(self.num_analysis))

    # -----------------
    # buttons
    def button0(self):
        print("button0")
        self.right_widget.clear()
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()
        self.tab5 = self.ui5()
        self.tab6 = self.ui6()
        self.tab7 = self.ui7()
        self.tab8 = self.ui8()
        self.tab9 = self.ui9()

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')
        self.right_widget.addTab(self.tab5, '')
        self.right_widget.addTab(self.tab6, '')
        self.right_widget.addTab(self.tab7, '')
        self.right_widget.addTab(self.tab8, '')
        self.right_widget.addTab(self.tab9, '')

        self.tab1.loadtable()
        self.right_widget.setCurrentIndex(0)
        self.tickerbutton()
        self.dict = {}
        self.btn_1_ticker.hide()
        self.btn_2_ticker.hide()
        self.btn_3_ticker.hide()
        self.btn_4_ticker.hide()
        self.btn_5_ticker.hide()
        self.btn_6_ticker.hide()
        self.btn_7_ticker.hide()

    def button1(self):
        self.right_widget.setCurrentIndex(1)
        self.tickerbutton()

    def button2(self):
        self.right_widget.setCurrentIndex(2)
        self.tickerbutton()

    def button3(self):
        self.right_widget.setCurrentIndex(3)
        self.tickerbutton()

    def button4(self):
        self.right_widget.setCurrentIndex(4)
        self.tickerbutton()

    def button5(self):
        self.right_widget.setCurrentIndex(5)
        self.tickerbutton()

    def button6(self):
        self.right_widget.setCurrentIndex(6)
        self.tickerbutton()

    def button7(self):
        self.right_widget.setCurrentIndex(7)
        # if len(self.dict.keys()) == 8:
        #     self.right_widget.setCurrentIndex(7)
        #     self.tickerbutton()
        # elif len(self.dict.keys()) == 7:
        #     self.shownotification('./Images/warning.png', "You didn't analyze.")
        # else:
        #     self.shownotification('./Images/warning.png', 'Input all parameters.')
    def btnsetting(self):
        self.right_widget.setCurrentIndex(8)

    def shownotification(self, iconpath, message):
        icon = QIcon(iconpath)
        custom_message_box = CustomMessageBox(icon, 'Custom Message', message, self)
        custom_message_box.setGeometry(1050, 20, 300, 70)
        custom_message_box.show()
    # -----------------
    # pages

    def ui1(self):
        main = FirstPageClass('./Images/designbackground.png', self.designpath, self)
        main.loadtable()
        return main

    def ui2(self):
        #         System
        main = QWidget()
        label = IntroLabel1(main)
        label.setText("System")
        label.move(440, 30)

        self.data_form_systemdesign = ["System Design",
                                       ["Heat Load", "W", "lineedit", "2800"],
                                       ["Input Fluid Temperature", "dC", "lineedit", '60']]
        self.form_systemdesign = InputForm(main, self.data_form_systemdesign)
        self.form_systemdesign.move(257, 100)



        def uimovenext():
            print("uimovenext")
            dict = {}
            if self.form_systemdesign.getValidation():
                dict = self.form_systemdesign.getData()
            else:
                self.btn_1_ticker.hide()
                self.movenext()
                return False
            self.btn_1_ticker.show()
            self.dict["System"] = dict
            self.movenext()
            return True

        def uimoveprevious():
            self.moveprevious()

        def setData(data):
            self.form_systemdesign.setData(data['System'])

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(225, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Next Step'))
        btn_next.move(575, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(uimovenext)
        return main

    def ui3(self):
        #       Fluid
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Fluid")
        label.move(440, 30)

        self.data_form_fluidproperties = ["Fuild Properties",
                                     ["Fluid Type",
                                      ["Water", "Methanol", "Ethylene Glycol", "Propylene Glycol", "Sodium Chloride",
                                       "Calcium Chloride"], "combobox"],
                                     ["Viscosity", "Pa*s", "lineedit", "0.011"],
                                     ["Specific Heat", "K/(Kg*dC)", "lineedit", "3344"],
                                     ["Density", "Kg/m^3", "lineedit", "1100"]
                                     ]
        self.form_fluidproperties = InputForm(main, self.data_form_fluidproperties)
        self.form_fluidproperties.move(257, 100)

        web_view = QWebEngineView(main)
        file_path = "D:\Heat Exchanger\Project\SGHEDA_v1.0\HTML\FluidTable1.html"
        web_view.load(QUrl.fromLocalFile(file_path))
        web_view.setStyleSheet('''
            background-color: rgba(0,0,0,0);
            color: white;
            border-radius: 10px;
        ''')
        web_view.setGeometry(100, 350, 800, 300)

        def uimovenext():
            print("uimovenext")
            dict = {}
            if self.form_fluidproperties.getValidation():
                dict = self.form_fluidproperties.getData()
            else:
                self.btn_2_ticker.hide()
                self.movenext()
                return False

            self.dict["Fluid"] = dict
            self.btn_2_ticker.show()
            self.movenext()
            return True

        def uimoveprevious():
            self.moveprevious()

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(225, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Next Step'))
        btn_next.move(575, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(uimovenext)
        return main

    def ui4(self):
        # Soil
        main = QWidget()

        label = IntroLabel1(main)
        label.setText(" Soil ")
        label.move(440, 30)

        self.data_form_soilthermalproperties = ["Soil Thermal Properties",
                                    ["Thermal Conductivity", "W/(m*K*⁰C)", "lineedit", "0.07"],
                                    ["Thermal Diffusivity", "m^2/h", 'lineedit', "0.62"],
                                    ["Ground Temperature", "⁰C", "lineedit", '30']
                                 ]
        self.form_soilthermalproperties = InputForm(main, self.data_form_soilthermalproperties)
        self.form_soilthermalproperties.move(257, 100)

        web_view = QWebEngineView(main)
        file_path = "D:\Heat Exchanger\Project\SGHEDA_v1.0\HTML\SoilTable1.html"
        web_view.load(QUrl.fromLocalFile(file_path))
        web_view.setStyleSheet('''
                    background-color: rgba(0,0,0,0);
                    color: white;
                    border-radius: 10px;
                ''')
        web_view.setGeometry(100, 300, 800, 350)

        def uimovenext():
            print("uimovenext")
            dict = {}
            if self.form_soilthermalproperties.getValidation():
                dict = self.form_soilthermalproperties.getData()
            else:
                self.btn_3_ticker.hide()
                self.movenext()
                return False

            self.dict["Soil"] = dict
            self.btn_3_ticker.show()
            self.movenext()
            return True

        def uimoveprevious():
            self.moveprevious()

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(225, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Next Step'))
        btn_next.move(575, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(uimovenext)

        return main

    def ui5(self):
        # Pipe
        main = QWidget()

        label = IntroLabel1(main)
        label.setText(" Pipe")
        label.move(440, 30)

        self.data_form_pipeproperties = ["Pipe Properties",
                                    ["Pipe Size", ["3/4 in. (20mm)", "1 in. (25mm)", "1 1/4 in. (32mm)", "1 1/2 in. (40mm)"], "combobox"],
                                    ["Outer Diameter", "m", "lineedit", '0.021'],
                                    ["Inner Diameter", "m", "lineedit", '0.026'],
                                    ["Pipe Type", ["SDR11", "SDR11-OD", "SDR13.5", "SDR13.5-OD"], "combobox"],
                                    ["Flow Type", ["Turbulent", "Transition", "Laminar"], "combobox"],
                                    ["Pipe Conductivity", "W/(m*K)", "lineedit", '0.14']
                                  ]
        self.form_pipeproperties = InputForm(main, self.data_form_pipeproperties)
        self.form_pipeproperties.move(257, 100)

        self.data_form_pipeconfiguration = ["Pipe Configuration",
                                        ['Buried Depth', 'm', 'lineedit', '2.0']]
        self.form_pipeconfiguration = InputForm(main, self.data_form_pipeconfiguration)
        self.form_pipeconfiguration.move(287, 450)

        def uimovenext():
            print("uimovenext")
            dict = {}
            if self.form_pipeproperties.getValidation():
                dict = self.form_pipeproperties.getData()
            else:
                self.btn_4_ticker.hide()
                self.movenext()
                return False
            if self.form_pipeconfiguration.getValidation():
                dict.update(self.form_pipeconfiguration.getData())
            else:
                self.btn_4_ticker.hide()
                self.movenext()
                return False

            self.dict["Pipe"] = dict
            self.btn_4_ticker.show()
            self.movenext()
            return True

        def uimoveprevious():
            self.moveprevious()

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(225, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Next Step'))
        btn_next.move(575, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(uimovenext)

        return main

    def ui6(self):
        # Pump
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("  Pump")
        label.move(440, 30)

        self.data_form_circulationpumps = ["Circulation Pump",
                                      ["Required Power", 'W', "lineedit", '600'],
                                      ["Fluid Velocity", "m/s", 'lineedit', '1.5'],
                                      ['Pump Motor Efficiency', '%', 'lineedit', '85']
                                      ]
        self.form_circulationpumps = InputForm(main, self.data_form_circulationpumps)
        self.form_circulationpumps.move(267, 100)
        timer = QTimer()

        def uimoveprevious():
            self.moveprevious()

        def end_loading():

            self.left_widget.setEnabled(True)
            loading_label.setVisible(False)
            btn_loading_stop.setVisible(False)
            movie.stop()
            timer.stop()
            self.result()
            self.btn_6_ticker.show()

        def start_loading():
            print("Design")
            if self.num_design == '∞' or self.num_design > 0:
                dict = {}
                if self.form_circulationpumps.getValidation():
                    dict = self.form_circulationpumps.getData()
                else:
                    self.shownotification('./Images/warning.png', "Input all parameters.")
                    return False
                self.dict["Pump"] = dict
                self.btn_5_ticker.show()

                if len(self.dict.keys()) < 5:
                    print('Design1', len(self.dict.keys()))
                    self.shownotification('./Images/warning.png', "Input all parameters.")
                    return False

                loading_label.setVisible(True)
                self.left_widget.setEnabled(False)
                btn_loading_stop.setVisible(True)
                movie.start()
                timer.timeout.connect(end_loading)
                timer.start(2000)
            else:
                self.shownotification('./Images/error.png', "Get license!")

        def loading_stop():
            self.left_widget.setEnabled(True)
            loading_label.setVisible(False)
            btn_loading_stop.setVisible(False)
            movie.stop()
            timer.stop()

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(225, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Design'))
        btn_next.move(575, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(start_loading)

        movie = QMovie('./Images/loading.gif')
        loading_label = QLabel(main)
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setFixedSize(730, 730)
        loading_label.setVisible(False)
        loading_label.setMovie(movie)
        loading_label.move(120, 0)

        btn_loading_stop = ImageButton1(main, './Images/x02.png')
        btn_loading_stop.setToolTip('Cancel Calculation')
        btn_loading_stop.move(900, 30)
        btn_loading_stop.clicked.connect(loading_stop)
        btn_loading_stop.setVisible(False)

        return main

    def ui7(self):
        # Result
        main = QWidget()

        label = IntroLabel1(main)
        label.setText(" Result")
        label.move(440, 30)

        main.setStyleSheet('''
            color: white;
        ''')

        self.data_form_designdimensions = ["Design Dimensions",
                                      ["Ring Diameter", 'm', "lineedit", '0.75'],
                                      ["Pitch", 'm', "lineedit", '0.4'],
                                      ["Number of Ring", '', 'lineedit', '5'],
                                      ["Pipe Length", 'm', "lineedit", '200'],
                                      ['Inlet Temperature', '⁰C', 'lineedit', '70'],
                                      ['System Flow Rate', 'm/s', 'lineedit', '10']
                                      ]
        self.form_designdimensions = InputForm(main, self.data_form_designdimensions)
        self.form_designdimensions.move(277, 100)

        label_description = IntroLabel3(main)
        label_description.setText('Description')
        label_description.setAlignment(Qt.AlignCenter)
        label_description.move(440, 420)

        self.textedit_description = CustomQTextEdit(main)
        self.textedit_description.setPlaceholderText('Design GHE for blockchain mining equipment')
        self.textedit_description.setGeometry(150, 455, 700, 150)

        def uisavedesign():
            if self.textedit_description.toPlainText() == "":
                self.textedit_description.setText('Design GHE for blockchain mining equipment')
            description = self.textedit_description.toPlainText()
            self.dict["Description"] = description

            if len(self.dict.keys()) == 7:
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                file_path, _ = QFileDialog.getSaveFileName(main, "Save File", "", "Text Files *.gld;;",
                                                           options=options)
                print(file_path)
                if file_path:
                    temp_file_path = file_path.split('/')[-1].split('.')
                    if len(temp_file_path) == 1:
                        file_path = file_path + '.gld'
                    with open(file_path, 'w') as file:
                        file.write(json.dumps(self.dict))
                    with open(self.designpath, 'r') as tablefile:
                        try:
                            tablecontent = json.load(tablefile)
                        except Exception as e:
                            tablecontent = {}
                            print("Design file is empty!")
                    with open(self.designpath, 'w') as savefile:
                        tablecontent[file_path] = description
                        savefile.write(json.dumps(tablecontent))
                return True
            else:
                self.shownotification('./Images/warning.png', "Input all parameters.")
                return False
        def gotoanalysis():
            if len(self.dict.keys()) == 7:
                self.analysis_calculation_result = True
                self.analysis()
                end_loading()
                self.right_widget.setCurrentIndex(7)
                self.tickerbutton()
                return True
            else:
                self.shownotification('./Images/warning.png', 'Input all parameters.')
                return False

        def end_loading():
            self.analysis_calculation_process = False
            self.left_widget.setEnabled(True)
            loading_label.setVisible(False)
            btn_loading_stop.setVisible(False)
            movie.stop()
            self.right_widget.setCurrentIndex(6)
            self.btn_7_ticker.show()


        def start_loading():
            print("start loading")
            self.analysis_calculation_process = True
            loading_label.setVisible(True)
            self.left_widget.setEnabled(False)
            btn_loading_stop.setVisible(True)
            movie.start()
            self.tickerbutton()

        def start_analysis():
            if self.num_analysis == '∞' or self.num_analysis > 0:
                if self.textedit_description.toPlainText() == "":
                    self.textedit_description.setText('Design GHE for blockchain mining equipment')
                description = self.textedit_description.toPlainText()
                self.dict["Description"] = description
                if len(self.dict.keys()) == 7:
                    start_loading()
                    thread = threading.Thread(target=gotoanalysis)
                    thread.start()

                    # database update
                    if self.num_analysis == "∞":
                        print('full license access')
                    else:
                        self.num_analysis -= 1
                        self.database_set_data()
                        self.combobox_selection_changed()
                else:
                    self.shownotification('./Images/warning.png', 'Input all parameters.')
            else:
                self.shownotification('./Images/error.png', 'Get license!')


        btn_save = MainButton1(main)
        btn_save.setText(main.tr('Save design'))
        btn_save.move(150, 670)
        btn_save.resize(170, 55)
        btn_save.clicked.connect(uisavedesign)

        btn_redesign = MainButton1(main)
        btn_redesign.setText(main.tr('Redesign'))
        btn_redesign.move(412, 670)
        btn_redesign.resize(170, 55)
        btn_redesign.clicked.connect(self.button0)

        btn_gotoanalysis = MainButton1(main)
        btn_gotoanalysis.setText(main.tr('Go to Analysis'))
        btn_gotoanalysis.move(675, 670)
        btn_gotoanalysis.resize(170, 55)
        btn_gotoanalysis.clicked.connect(start_analysis)

        movie = QMovie('./Images/loading.gif')
        loading_label = QLabel(main)
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setFixedSize(730, 730)
        loading_label.setVisible(False)
        loading_label.setMovie(movie)
        loading_label.move(120, 0)

        btn_loading_stop = ImageButton1(main, './Images/x02.png')
        btn_loading_stop.setToolTip('Cancel Calculation')
        btn_loading_stop.move(900, 30)
        btn_loading_stop.clicked.connect(end_loading)
        btn_loading_stop.setVisible(False)

        return main

    def ui8(self):
        # Analysis
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Analysis")
        label.move(440, 30)
        
        self.plt_gfunction = pg.PlotWidget(main)
        self.plt_gfunction.setTitle("G-function")
        self.plt_gfunction.setLabel('left', 'g-function')
        self.plt_gfunction.setLabel('bottom', 'Time')
        self.plt_gfunction.setBackground('#2C3751')
        self.plt_gfunction.setGeometry(150, 100, 700, 400)

        # self.plt_temperaturepertubation = pg.PlotWidget(main)


        btn_redesign = MainButton1(main)
        btn_redesign.setText(main.tr('Redesign'))
        btn_redesign.move(410, 670)
        btn_redesign.resize(170, 55)
        btn_redesign.clicked.connect(self.button0)

        # btn_gotoanalysis = MainButton1(main)
        # btn_gotoanalysis.setText(main.tr('Go to Analysis'))
        # btn_gotoanalysis.move(625, 670)
        # btn_gotoanalysis.resize(170, 55)
        # # btn_gotoanalysis.clicked.connect(uigotoanalysis)

        scroll_area.setWidget(main)
        return scroll_area

    def ui9(self):
        # Settings
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Settings")
        label.move(425, 30)

        self.license_info = LicenseForm(main, self)
        self.license_info.resize(600, 200)
        self.license_info.move(200, 100)

        self.data_time_setting = ['Time Setting',
                                  ['Prediction Time', ['1 month', '2 month', '6 month', '1 year'], 'combobox']
                                  ]

        self.time_setting = InputForm(main, self.data_time_setting)
        self.time_setting.resize(300, 100)
        self.time_setting.move(160, 350)

        self.personal_setting = PersonalForm(main)
        self.personal_setting.resize(300, 137)
        self.personal_setting.move(160, 470)

        self.data_userinfo = ['User Info',
                              ['Username', '', 'lineedit', '**** ****'],
                              ['Gmail','', 'lineedit', 'default@gmail.com'],
                              ['Purpose', '', 'lineedit', 'Residental Building'],
                              ['Country', '', 'lineedit', 'Canada'],
            ['Phone', '', 'lineedit', '1010101010']
            ]
        self.userinfo = InputForm(main, self.data_userinfo)
        self.userinfo.move(500, 350)

        return main

    def movenext(self):
        self.right_widget.setCurrentIndex(self.right_widget.currentIndex() + 1)
        self.tickerbutton()

    def moveprevious(self):
        self.right_widget.setCurrentIndex(self.right_widget.currentIndex() - 1)
        self.tickerbutton()

    def loaddata(self):
        print("loaddata")
        try:
            with open(self.currentgldpath, 'r') as f:
                context = json.load(f)
        except:
            self.shownotification('./Images/warning.png', "Can't find the file!")
        print(context)
        if len(context) < 6:
            self.shownotification("./Images/error.png", "This file is corrupted!")
        else:
            self.form_systemdesign.setData1(list(context['System'].values()))
            self.btn_1_ticker.show()
            self.dict['System'] = context['System']
            self.form_fluidproperties.setData1(list(context['Fluid'].values()))
            self.btn_2_ticker.show()
            self.dict['Fluid'] = context['Fluid']
            self.form_soilthermalproperties.setData1(list(context['Soil'].values()))
            self.btn_3_ticker.show()
            self.dict['Soil'] = context['Soil']
            self.form_pipeproperties.setData1(list(context['Pipe'].values())[:6])
            self.btn_4_ticker.show()
            self.dict['Pipe'] = context['Pipe']
            self.form_pipeconfiguration.setData1(context['Pipe']['Buried Depth'])
            self.form_circulationpumps.setData1(list(context['Pump'].values()))
            self.btn_5_ticker.show()
            self.dict['Pump'] = context['Pump']
            self.form_designdimensions.setData1(list(context['Results'].values()))
            self.form_designdimensions.setReadOnly(True)
            self.textedit_description.setText(context['Description'])
            self.btn_6_ticker.show()
            self.dict['Results'] = context['Results']
            self.dict['Description'] = context['Description']
            # print(context)
            self.right_widget.setCurrentIndex(6)
    def redirect_to_feedback(self):
        webbrowser.open('https://www.figma.com/file/dCCAp7MQBZ4RTQteuPaS4s/SGHEDA_v1.1?type=design&node-id=0-1&mode=design&t=67IVnjAvS4q6OyWX-0')

    def redirect_to_help(self):
        webbrowser.open('https://www.figma.com/file/dCCAp7MQBZ4RTQteuPaS4s/SGHEDA_v1.1?type=design&node-id=0-1&mode=design&t=67IVnjAvS4q6OyWX-0')

    def exitbutton(self):
        self.parent.exit()

    def sizing(self):
        # System
        try:
            E_heat = float(self.dict['System']['Heat Load'])  # heat load [W*h]
            T_in = float(self.dict['System']['Input Fluid Temperature'])  # Hot Fluid Temperature 60~65dC, 140~150dF

            # Fluid
            mu = float(self.dict["Fluid"]["Viscosity"])
            c_p = float(self.dict["Fluid"]["Specific Heat"])
            rho = float(self.dict["Fluid"]["Density"])

            # Soil
            k_soil = float(self.dict["Soil"]["Thermal Conductivity"])
            T_g = float(self.dict["Soil"]["Ground Temperature"])

            # print(E_heat, T_in, mu, c_p, rho, k_soil, T_g)

            # Pipe
            D_i = float(self.dict['Pipe']['Inner Diameter'])
            D_o = float(self.dict['Pipe']['Outer Diameter'])
            f_type = self.dict['Pipe']['Flow Type']
            k_pipe = float(self.dict['Pipe']['Pipe Conductivity'])
            d = float(self.dict['Pipe']['Buried Depth'])

            # Pump
            V = float(self.dict["Pump"]["Fluid Velocity"])  # modify
            p = float(self.dict['Pump']['Required Power'])

        except Exception as e:
            print('Exception: ', traceback.format_exc())
            self.shownotification("./Images/warning.png", "Didn't input all variables.")
            return False
        print('after input variable')
        try:
        # Resistance
            R_e = rho * V * D_i / mu  # Reynolds number    Re<2100 laminar regime; 2100<Re<10000: transitional regime;
            # Re>10000 turbulent regime
            P_r = mu * c_p / k_pipe  # Prandtl number
            h_w = 0.023 * R_e ** 0.8 * P_r ** 0.3 * k_pipe / D_i  # heat transfer coefficient [W/(m^2*k)]

            R_conv = 1 / (3.14159 * D_i * h_w)
            R_pipe = math.log(D_o / D_i) / (2 * 3.14159 * k_pipe)
            S = 2 * 3.14159 / math.log((2 * d / D_o) + math.sqrt((2 * d / D_o) ** 2 - 1))  # conduction shape factor of
            # the pipe
            R_soil = 1 / (S * k_soil)

            R_total = R_conv + R_pipe + R_soil

            # Length calculation
            m_w = rho * V * 3.14159 * (D_i / 2) ** 2
            T_out = T_in - E_heat / (m_w * c_p)
            theta_w_in = T_in - T_g
            theta_w_out = T_out - T_g

            L = (m_w * c_p * R_total) * math.log(theta_w_in / theta_w_out)
            L = L/4
            print("length of pipe:", L)
            ring_diameter = 0.75*T_in/T_out
            pitch = 0.4*T_in/T_out

            dict = {}
            dict['Ring Diameter'] = str(ring_diameter)
            dict['Pitch'] = str(pitch)
            dict['Number of Ring'] = str(L/(3.14*ring_diameter + pitch))
            dict['Pipe Length'] = str(L + 2*d)
            dict['Inlet Temperature'] = str(T_in)
            dict['System Flow Rate'] = str(V)
            self.dict['Results'] = dict

            if self.num_analysis == '∞':
                print('full license access')
            else:
                self.num_design -= 1
                self.database_set_data()
                self.combobox_selection_changed()
            return True
        except Exception as e:
            print('Size Calculation Error:', traceback.format_exc())
            self.shownotification("./Image/error.png", "Can't calculate design parameters")
            return False

    def result(self):
        if self.sizing():
            self.form_designdimensions.setData1(list(self.dict["Results"].values()))
            self.form_designdimensions.setReadOnly(True)
            self.right_widget.setCurrentIndex(6)
            self.tickerbutton()
        else:
            print('Show Notification')
    def analysis(self):
        print('Analysis')
        N_ring = 5
        R = 1  # m
        pitch: np.float16 = 0.2  # m
        # alpha = 1e-6  # m2/s
        t_series = np.arange(0.01, 30, 1)  # consider alpha
        t_1 = int(1e6)
        h = 2  # m

        def sqrt_float16(x):
            return np.sqrt(x).astype(np.float16)

        def erfc_float16(x):
            return erfc(x).astype(np.float16)

        def cos_float16(x):
            return np.cos(x).astype(np.float16)

        def sin_float16(x):
            return np.sin(x).astype(np.float16)

        def quadself(f, a, b, c, d, nx, ny):
            # Function to approximate the double integral
            dx: np.float16 = (b - a) / nx
            dy: np.float16 = (d - c) / ny

            integral_sum: np.float16 = 0.0

            for i in range(nx):
                x = a + (i + 0.5) * dx

                for j in range(ny):
                    y = c + (j + 0.5) * dy
                    integral_sum += f(x, y)

            integral_sum *= dx * dy

            return integral_sum

        start_time = time.time()

        # gs_series = []
        # for N_ring in N_ring_series:
        gs_series = []
        for t in t_series:
            gs: np.float16 = 0
            for i in range(1, N_ring + 1):
                for j in range(1, N_ring + 1):
                    if self.analysis_calculation_process:
                        if i != j:

                            def d(w: np.float16, phi: np.float16):
                                return sqrt_float16((pitch * (i - j) + R * (cos_float16(phi) - cos_float16(w))) ** 2 +
                                                    (R * (sin_float16(phi) - sin_float16(w))) ** 2)

                            def fun(w: np.float16, phi: np.float16):
                                return erfc_float16(d(w, phi) / (2 * sqrt_float16(t))) / d(w, phi) - erfc_float16(
                                    sqrt_float16(d(w, phi) ** 2 + 4 * h ** 2) / (2 * sqrt_float16(t))) / sqrt_float16(
                                    d(w, phi) ** 2 + 4 * h ** 2)

                            # b, _ = dblquad(fun, 0, 2 * np.pi, lambda phi: 0, lambda phi: 2 * np.pi, epsabs=1e-2, epsrel=1e-2)
                            b = quadself(fun, 0, 2 * np.pi, 0, 2 * np.pi, 20, 20)
                            # print(b)
                            gs += np.float16(b)
                    else:
                        return False
            # print(f"gs: {gs}")
            gs_series.append(gs)

        end_time = time.time()
        elapsed_time = end_time - start_time

        print("Elapsed time: {:.2f}".format(elapsed_time))
        # x = np.linspace(0, 2*np.pi, 1000)
        # y = np.sin(x)
        self.plt_gfunction.clear()
        self.plt_gfunction.plot(t_series*1000000, gs_series, pen='b')
        self.dict["Analysis"] = {"Elapsed time": str(elapsed_time)}

        return True

    def btnexit(self):
        self.setEnabled(False)
        notification = ExitNotification(self)
        result = notification.exec_()

        if result == QMessageBox.No:
            self.setEnabled(True)
            return True
        
        elif result == QMessageBox.Yes:
            sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DesignClass()
    ex.show()
    sys.exit(app.exec_())
