import json
import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMainWindow, QTabWidget, \
    QHBoxLayout, QSizePolicy, QComboBox, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtCore import Qt, QSize

from buttonclass import ImageButton, ExtraButton, SquareButton, ExitButton, MainButton1
from firstpageclass import FirstPageClass
from inputformclass import InputForm
from labelclass import IntroLabel1, TickerLabel
from notificationclass import CustomMessageBox


class DesignClass(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.tabstack = []
        self.dict = {}
        self.designpath = './Logs/designpath.json'
        self.num_design = 5
        self.num_analysis = 4
        self.currentgldpath = ''

        # set the size of window
        self.setFixedSize(1210, 790)

        # Set the background color of the main window
        self.setStyleSheet("background-color: #1F2843; border: none")

        # add all widgets

        self.left_widget = QWidget()
        self.left_widget.setStyleSheet("""
            background-color: #2C3751;
            border-radius: 10px;
        """)

        # Image button
        self.btn_home = ImageButton(self.left_widget, './Images/logo03.png')
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
                selection-background-color: red;
                padding: 1px 1px 1px 1px;
                min-width: 0em;
                font-size: 16px;
            }
            
            QComboBox:hover {
                color: #2978FA;
            }
            
            QComboBox::drop-down {
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
        self.label_num.setGeometry(130, 155, 60, 30)
        self.label_num.setStyleSheet("""
            QPushButton {
                background-color: #374866;
                color: white;
                font-size: 16px;
                border-radius: 13px
            }
            QPushButton:hover {
                background-color: #5A6B90;
            }
        """)
        self.label_num.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.btn_1 = SquareButton(self.left_widget, './Images/fluid02.png')
        self.btn_1.setText(' Fluid')
        self.btn_1.setGeometry(0, 200, 212, 50)
        self.btn_2 = SquareButton(self.left_widget, './Images/soil01.png')
        self.btn_2.setText(' Soil')
        self.btn_2.setGeometry(0, 250, 212, 50)
        self.btn_3 = SquareButton(self.left_widget, './Images/pipe01.png')
        self.btn_3.setText(' Piping')
        self.btn_3.setGeometry(0, 300, 212, 50)
        self.btn_4 = SquareButton(self.left_widget, './Images/configuration01.png')
        self.btn_4.setText(' Configuration')
        self.btn_4.setGeometry(0, 350, 212, 50)
        self.btn_5 = SquareButton(self.left_widget, './Images/power02.png')
        self.btn_5.setText(' Extra Kw')
        self.btn_5.setGeometry(0, 400, 212, 50)
        self.btn_6 = SquareButton(self.left_widget, './Images/result01.png')
        self.btn_6.setText(' Result')
        self.btn_6.setGeometry(0, 450, 212, 50)
        self.btn_7 = SquareButton(self.left_widget, './Images/analysis05.png')
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
        self.tab5 = self.ui5()
        self.tab6 = self.ui6()
        self.tab7 = self.ui7()
        self.tab8 = self.ui8()

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

        self.button0()
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
        main_layout.setStretch(0, 22)
        main_layout.setStretch(1, 100)
        self.setLayout(main_layout)

    # -----------------
    # ticker button
    def tickerbutton(self):
        currentIndex = self.right_widget.currentIndex()
        if self.right_widget.currentIndex() == 0:
            self.slide_label.hide()
        else:
            self.slide_label.move(0, 200 + 50 * (currentIndex - 1))
            self.slide_label.show()

    # combobox
    def combobox_selection_changed(self):
        selected_text = self.combobox_selection.currentText()
        print(selected_text)
        if selected_text == '  Design ':
            self.label_num.setText(' ' + str(self.num_design))
        else:
            self.label_num.setText(' ' + str(self.num_analysis))

    # -----------------
    # buttons
    def button0(self):
        print("button0")
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
        if len(self.dict.keys()) == 7:
            self.right_widget.setCurrentIndex(7)
            self.tickerbutton()
        else:
            icon = QIcon('./Images/logo03.png')
            custom_message_box = CustomMessageBox(icon, 'Custom Message', 'Please input design \n'
                                                                          '    parameter.', self)
            custom_message_box.setGeometry(900, 20, 300, 70)
            custom_message_box.show()
            print("notification")

    # -----------------
    # pages

    def ui1(self):
        main = FirstPageClass('./Backgrounds/designbackground.png', self.designpath, self)
        main.loadtable()
        return main

    def ui2(self):
        #         Fluid
        main = QWidget()
        label = IntroLabel1(main)
        label.setText("Fluid")
        label.move(400, 30)

        data_form_fluidsystemdesign = ["System Design",
                                       ["Inlet Temperature", "dF", "lineedit", "90.0"],
                                       ["Flow Rate", "gpm/ton", "lineedit", '3.0'],
                                       ["Fluid type", ["Water", "Methanol"], "combobox"]]
        form_fluidsystemdesign = InputForm(main, data_form_fluidsystemdesign)
        form_fluidsystemdesign.move(200, 100)

        data_form_fluidproperties = ["Fuild Properties",
                                     ["Fluid Type",
                                      ["Water", "Methanol", "Ethylene Glycol", "Propylene Glycol", "Sodium Chloride",
                                       "Calcium Chloride"], "combobox"],
                                     ["Design Outlet Temperature", "⁰F", "lineedit", "60.0"],
                                     ["Specific Heat", "Btu/(⁰F*lbm)", "lineedit", "1.01"],
                                     ["Density", "lb/ft^3", "lineedit", "60.6"]
                                     ]
        form_fluidproperties = InputForm(main, data_form_fluidproperties)
        form_fluidproperties.move(150, 350)

        def uimovenext():
            print("uimovenext")
            dict = {}
            if form_fluidsystemdesign.getValidation():
                dict[data_form_fluidsystemdesign[0]] = form_fluidsystemdesign.getData()
            else:
                self.btn_1_ticker.hide()
                self.movenext()
                return False
            if form_fluidproperties.getValidation():
                dict[data_form_fluidproperties[0]] = form_fluidproperties.getData()
            else:
                self.btn_1_ticker.hide()
                self.movenext()
                return False
            self.btn_1_ticker.show()
            self.dict["fluid"] = dict
            self.movenext()
            return True

        def uimoveprevious():
            self.moveprevious()

        def setData(data):
            form_fluidsystemdesign.setData(data['System Design'])
            form_fluidproperties.setData(data['Fluid Properties'])

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(200, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Next Step'))
        btn_next.move(550, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(uimovenext)
        return main

    def ui3(self):
        #       Soil
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Soil")
        label.move(400, 30)

        data_form_undisturbedgroundtemperature = ["Undisturbed Ground Temperature",
                                                  ["Ground Temperature", "⁰F", "lineedit", '62.0']
                                                  ]
        form_undisturbedgroundtemperature = InputForm(main, data_form_undisturbedgroundtemperature)
        form_undisturbedgroundtemperature.move(200, 100)

        data_form_soilthermalproperties = ["Soil Thermal Properties",
                                           ["Thermal Conductivity", "Btu/(h*ft*⁰F)", "lineedit", '0.75'],
                                           ["Thermal Diffusivity", "ft^2/day", "lineedit", '0.62']
                                           ]
        form_soilthermalproperties = InputForm(main, data_form_soilthermalproperties)
        form_soilthermalproperties.move(150, 350)

        def uimovenext():
            print("uimovenext")
            dict = {}
            if form_undisturbedgroundtemperature.getValidation():
                dict[data_form_undisturbedgroundtemperature[0]] = form_undisturbedgroundtemperature.getData()
            else:
                self.btn_2_ticker.hide()
                self.movenext()
                return False
            if form_soilthermalproperties.getValidation():
                dict[data_form_soilthermalproperties[0]] = form_soilthermalproperties.getData()
            else:
                self.btn_2_ticker.hide()
                self.movenext()
                return False

            self.dict["soil"] = dict
            self.btn_2_ticker.show()
            self.movenext()
            return True

        def uimoveprevious():
            self.moveprevious()

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(200, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Next Step'))
        btn_next.move(550, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(uimovenext)
        return main

    def ui4(self):
        # Piping
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Piping")
        label.move(400, 30)

        data_form_trenchlayout = ["Trench Layout",
                                  ["Pipe Resistance", "h*ft*⁰F/Btu", "lineedit", '0.156'],
                                  ["Pipe Size",
                                   ["3/4 in. (20mm)", "1 in. (25mm)", "1 1/4 in. (32mm)", "1 1/2 in. (40mm)"],
                                   "combobox"],
                                  ["Pipe Type", ["SDR11", "SDR11-OD", "SDR13.5", "SDR13.5-OD"], "combobox"],
                                  ["Flow Type", ["Turbulent", "Transition", "Laminar"], "combobox"]
                                  ]
        form_trenchlayout = InputForm(main, data_form_trenchlayout)
        form_trenchlayout.move(200, 100)

        def uimovenext():
            print("uimovenext")
            dict = {}
            if form_trenchlayout.getValidation():
                dict[data_form_trenchlayout[0]] = form_trenchlayout.getData()
            else:
                self.btn_3_ticker.hide()
                self.movenext()
                return False

            self.dict["Piping"] = dict
            self.btn_3_ticker.show()
            self.movenext()
            return True

        def uimoveprevious():
            self.moveprevious()

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(200, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Next Step'))
        btn_next.move(550, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(uimovenext)

        return main

    def ui5(self):
        # Configuration
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Configuration")
        label.move(400, 30)

        data_form_pipeconfiguration = ["Pipe Configuration",
                                       ["Pipe Configuration",
                                        ['Slinky Horizontal GHE', 'Slinky Vertical GHE', 'Earth Basket'], "combobox"]
                                       ]
        form_pipeconfiguration = InputForm(main, data_form_pipeconfiguration)
        form_pipeconfiguration.move(200, 100)

        data_form_modelingtimeperiod = ["Modeling Time Period",
                                        ['Prediction Time', 'years', 'lineedit', '1.0']]
        form_modelingtimeperiod = InputForm(main, data_form_modelingtimeperiod)
        form_modelingtimeperiod.move(150, 350)

        def uimovenext():
            print("uimovenext")
            dict = {}
            if form_pipeconfiguration.getValidation():
                dict[data_form_pipeconfiguration[0]] = form_pipeconfiguration.getData()
            else:
                self.btn_4_ticker.hide()
                self.movenext()
                return False
            if form_modelingtimeperiod.getValidation():
                dict[data_form_modelingtimeperiod[0]] = form_modelingtimeperiod.getData()
            else:
                self.btn_4_ticker.hide()
                self.movenext()
                return False

            self.dict["Configuration"] = dict
            self.btn_4_ticker.show()
            self.movenext()
            return True

        def uimoveprevious():
            self.moveprevious()

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(200, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Next Step'))
        btn_next.move(550, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(uimovenext)

        return main

    def ui6(self):
        # Extra KW
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Extra KW")
        label.move(400, 30)

        data_form_circulationpumps = ["Circulation Pumps",
                                      ["Required Input Power", 'KW', "lineedit", '0.0'],
                                      ["Pump Power", "hP", 'lineedit', '0.0'],
                                      ['Pump Motor Efficiency', '%', 'lineedit', '85']
                                      ]
        form_circulationpumps = InputForm(main, data_form_circulationpumps)
        form_circulationpumps.move(200, 100)

        data_form_additionalpowerrequirements = ["Modeling Power",
                                                 ['Addtional Power', 'KW', 'lineedit', '0.0']]
        form_additionalpowerrequirements = InputForm(main, data_form_additionalpowerrequirements)
        form_additionalpowerrequirements.move(150, 350)

        def uimovenext():
            print("uimovenext")
            dict = {}
            if form_circulationpumps.getValidation():
                dict[data_form_circulationpumps[0]] = form_circulationpumps.getData()
            else:
                self.btn_5_ticker.hide()
                self.movenext()
                return False
            if form_additionalpowerrequirements.getValidation():
                dict[data_form_additionalpowerrequirements[0]] = form_additionalpowerrequirements.getData()
            else:
                self.btn_5_ticker.hide()
                self.movenext()
                return False

            self.dict["Extra KW"] = dict
            self.btn_5_ticker.show()
            self.movenext()
            return True

        def uimoveprevious():
            self.moveprevious()

        btn_open = MainButton1(main)
        btn_open.setText(main.tr('Previous Step'))
        btn_open.move(200, 670)
        btn_open.resize(170, 55)
        btn_open.clicked.connect(uimoveprevious)

        btn_next = MainButton1(main)
        btn_next.setText(main.tr('Design'))
        btn_next.move(550, 670)
        btn_next.resize(170, 55)
        btn_next.clicked.connect(uimovenext)

        return main

    def ui7(self):
        # Results
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Results")
        label.move(400, 30)

        main.setStyleSheet('''
            color: white;
        ''')
        data_form_designdimensions = ["Design Dimensions",
                                      ["Trench Length", 'ft', "lineedit", '20'],
                                      ["Total Pipe Length", "ft", 'lineedit', '60'],
                                      ['Inlet Temperature', '⁰F', 'lineedit', '70'],
                                      ["Outlet Temperature", '⁰F', "lineedit", '40'],
                                      ["Peak Load", "Kbtu/Hr", 'lineedit', '30'],
                                      ['Power Consumption', 'KWh/day', 'lineedit', '10'],
                                      ['System Flow Rate', 'gpm', 'lineedit', '10']
                                      ]
        form_designdimensions = InputForm(main, data_form_designdimensions)
        form_designdimensions.move(200, 100)

        data_form_description = ['Design Description',
                                 ['Description', '', 'lineedit', 'design GHE for blockchain mining equipment']]
        form_description = InputForm(main, data_form_description)
        form_description.move(250, 450)

        def uisavedesign():
            print("uimovenext")
            dict = {}

            if form_designdimensions.getValidation():
                dict[data_form_designdimensions[0]] = form_designdimensions.getData()
            else:
                icon = QIcon('./Images/logo03.png')
                custom_message_box = CustomMessageBox(icon, 'Custom Message', 'You have to input values \n'
                                                                              '    correctly.', self)
                custom_message_box.setGeometry(900, 20, 300, 70)
                custom_message_box.show()
                return False
            print('1')
            if form_description.getValidation():
                description = form_description.getData()
            else:
                # notification
                icon = QIcon('./Images/logo03.png')
                custom_message_box = CustomMessageBox(icon, 'Custom Message', 'You have to input values \n'
                                                                              '    parameter.', self)
                custom_message_box.setGeometry(900, 20, 300, 70)
                custom_message_box.show()
                return False

            self.dict["Results"] = dict
            self.dict["Description"] = description
            # self.movenext()
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
                    tablecontent = json.load(tablefile)
                with open(self.designpath, 'w') as savefile:
                    tablecontent[file_path] = description["Description"]
                    savefile.write(json.dumps(tablecontent))
            return True

        def gotoanalysis():
            print("uimovenext")
            dict = {}

            if form_designdimensions.getValidation():
                dict[data_form_designdimensions[0]] = form_designdimensions.getData()
            else:
                self.btn_6_ticker.hide()
                icon = QIcon('./Images/logo03.png')
                custom_message_box = CustomMessageBox(icon, 'Custom Message', 'You have to input values \n'
                                                                              '    correctly.', self)
                custom_message_box.setGeometry(900, 20, 300, 70)
                custom_message_box.show()
                return False
            print('1')
            if form_description.getValidation():
                description = form_description.getData()
            else:
                self.btn_6_ticker.hide()
                # notification
                icon = QIcon('./Images/logo03.png')
                custom_message_box = CustomMessageBox(icon, 'Custom Message', 'You have to input values \n'
                                                                              '    parameter.', self)
                custom_message_box.setGeometry(900, 20, 300, 70)
                custom_message_box.show()
                return False

            self.dict["Results"] = dict
            self.dict["Description"] = description
            self.btn_6_ticker.show()
            self.button7()

        btn_save = MainButton1(main)
        btn_save.setText(main.tr('Save design'))
        btn_save.move(100, 670)
        btn_save.resize(170, 55)
        btn_save.clicked.connect(uisavedesign)

        btn_redesign = MainButton1(main)
        btn_redesign.setText(main.tr('Redesign'))
        btn_redesign.move(362, 670)
        btn_redesign.resize(170, 55)
        btn_redesign.clicked.connect(self.button0)

        btn_gotoanalysis = MainButton1(main)
        btn_gotoanalysis.setText(main.tr('Go to Analysis'))
        btn_gotoanalysis.move(625, 670)
        btn_gotoanalysis.resize(170, 55)
        btn_gotoanalysis.clicked.connect(gotoanalysis)

        return main

    def ui8(self):
        # Analysis
        main = QWidget()

        label = IntroLabel1(main)
        label.setText("Analysis")
        label.move(400, 30)

        btn_redesign = MainButton1(main)
        btn_redesign.setText(main.tr('Redesign'))
        btn_redesign.move(450, 670)
        btn_redesign.resize(170, 55)
        # btn_redesign.clicked.connect(uiredesign)

        btn_gotoanalysis = MainButton1(main)
        btn_gotoanalysis.setText(main.tr('Go to Analysis'))
        btn_gotoanalysis.move(625, 670)
        btn_gotoanalysis.resize(170, 55)
        # btn_gotoanalysis.clicked.connect(uigotoanalysis)

        return main

    def movenext(self):
        self.right_widget.setCurrentIndex(self.right_widget.currentIndex() + 1)
        self.tickerbutton()

    def moveprevious(self):
        self.right_widget.setCurrentIndex(self.right_widget.currentIndex() - 1)
        self.tickerbutton()

    def loaddata(self):
        with open(self.currentgldpath, 'r') as f:
            context = json.load(f)
        print(context)

    def exitbutton(self):
        self.parent.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DesignClass()
    ex.show()
    sys.exit(app.exec_())
