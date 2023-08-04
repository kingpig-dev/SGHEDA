import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMainWindow, QTabWidget, \
    QHBoxLayout, QSizePolicy, QComboBox
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtCore import Qt

from buttonclass import ImageButton, ExtraButton, SquareButton, ExitButton, MainButton1
from firstpageclass import FirstPageClass
from inputformclass import InputForm

class DesignClass(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.tabstack = []
        self.dict = {}

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
        # self.btn_home.clicked.connect(self.parent.dashboardUI)

        self.combobox_selection = QComboBox(self.left_widget)
        self.icon_design = QIcon('./Images/design.png')
        self.icon_analysis = QIcon('./Images/analysis02.png')
        self.combobox_selection.addItem(self.icon_design, '  Design ')
        self.combobox_selection.addItem(self.icon_analysis, ' Analysis ')
        self.combobox_selection.resize(110, 30)
        self.combobox_selection.setCursor(QCursor(Qt.PointingHandCursor))
        arrow_icon = QPixmap('./Images/down01.png')
        self.combobox_selection.setStyleSheet("""            
             QComboBox {
                color: #7C8AA7;
                background-color: #2C3751;
                selection-background-color: #555555;
                padding: 1px 18px 1px 3px;
                min-width: 6em;
                font-size: 16px;
            }
            
            QComboBox::drop-down {
                subcontrol-origin: padding;
                width: 15px;
                
                border: none;
            }
            
            QComoboBox::down-arrow {
                image: url('+arrow_icon+');
            }
        """)
        self.combobox_selection.currentIndexChanged.connect(self.combobox_selection_changed)
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
        self.btn_6 = SquareButton(self.left_widget, './Images/result01.png')
        self.btn_6.setText(' Result')
        self.btn_6.setGeometry(0, 450, 200, 50)

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
        self.tab5 = self.ui5()

        # right widget
        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')
        self.right_widget.addTab(self.tab5, '')

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
        main_layout.setStretch(0, 25)
        main_layout.setStretch(1, 100)
        self.setLayout(main_layout)

    # -----------------
    # combobox
    def combobox_selection_changed(self):
        selected_text = self.combobox_selection.currentText()
        if selected_text == "Design":
            self.right_widget.setCurrentIndex(0)
        else:
            self.parent.analysisUI()

    # -----------------
    # buttons

    def button1(self):
        self.right_widget.setCurrentIndex(1)

    def button2(self):
        self.right_widget.setCurrentIndex(2)

    def button3(self):
        self.right_widget.setCurrentIndex(3)

    def button4(self):
        self.right_widget.setCurrentIndex(4)
        # self.parent.dashboardUI()
    # -----------------
    # pages

    def ui1(self):
        main = FirstPageClass('./Backgrounds/designbackground.png', './Logs/designpath.json', self)
        return main

    def ui2(self):
        #         Fluid
        main = QWidget()
        data_form_fluidsystemdesign = ["System Design",
                                       ["Inlet Temperature", "dF", "lineedit", "90.0"],
                                       ["Flow Rate", "gpm/ton", "lineedit", '3.0'],
                                       ["Fluid type", ["Water", "Methanol"], "combobox"]]
        form_fluidsystemdesign = InputForm(main, data_form_fluidsystemdesign)
        form_fluidsystemdesign.move(200, 100)

        data_form_fluidproperties = ["Fuild Properties",
                                          ["Fluid Type", ["Water", "Methanol", "Ethylene Glycol", "Propylene Glycol", "Sodium Chloride", "Calcium Chloride"], "combobox"],
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
                return False
            if form_fluidproperties.getValidation():
                dict[data_form_fluidproperties[0]] = form_fluidproperties.getData()
            else:
                return False

            self.dict["fluid"] = dict
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

    def ui3(self):
        #       Soil
        main = QWidget()
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
                return False
            if form_soilthermalproperties.getValidation():
                dict[data_form_soilthermalproperties[0]] = form_soilthermalproperties.getData()
            else:
                return False

            self.dict["soil"] = dict
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

        data_form_trenchlayout = ["Trench Layout",
                                             ["Pipe Resistance", "h*ft*⁰F/Btu", "lineedit", '0.156'],
                                             ["Pipe Size", ["3/4 in. (20mm)", "1 in. (25mm)", "1 1/4 in. (32mm)", "1 1/2 in. (40mm)"], "combobox"],
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
                return False

            self.dict["soil"] = dict
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

        data_form_pipeconfiguration = ["Pipe Configuration",
                                 ["Pipe Configuration", ['Slinky Horizontal GHE', 'Slinky Vertical GHE', 'Earth Basket'], "combobox"]
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
                return False
            if form_modelingtimeperiod.getValidation():
                dict[data_form_modelingtimeperiod[0]] = form_modelingtimeperiod.getData()
            else:
                return False
            self.dict["soil"] = dict
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

    # def ui6(self):
    #     # Extra KW
    #     main = QWidget()
    #
    #     data_form_circulationpumps = ["Circulation Pumps",
    #                                   ["Required Input Power", 'KW', "lineedit", '0.0'],
    #                                   ["Pump Power", "hP", 'lineedit', '0.0'],
    #                                   ['Pump Motor Efficiency']
    #                              ]
    #     form_circulationpumps = InputForm(main, data_form_pipeconfiguration)
    #     form_circulationpumps.move(200, 100)
    #
    #     data_form_modelingtimeperiod = ["Modeling Time Period",
    #                                     ['Prediction Time', 'years', 'lineedit', '1.0']]
    #     form_modelingtimeperiod = InputForm(main, data_form_modelingtimeperiod)
    #     form_modelingtimeperiod.move(150, 350)
    #
    #     def uimovenext():
    #         print("uimovenext")
    #         dict = {}
    #         if form_pipeconfiguration.getValidation():
    #             dict[data_form_pipeconfiguration[0]] = form_pipeconfiguration.getData()
    #         else:
    #             return False
    #         if form_modelingtimeperiod.getValidation():
    #             dict[data_form_modelingtimeperiod[0]] = form_modelingtimeperiod.getData()
    #         else:
    #             return False
    #         self.dict["soil"] = dict
    #         self.movenext()
    #         return True

        # def uimoveprevious():
        #     self.moveprevious()
        #
        # btn_open = MainButton1(main)
        # btn_open.setText(main.tr('Previous Step'))
        # btn_open.move(200, 670)
        # btn_open.resize(170, 55)
        # btn_open.clicked.connect(uimoveprevious)
        #
        # btn_next = MainButton1(main)
        # btn_next.setText(main.tr('Next Step'))
        # btn_next.move(550, 670)
        # btn_next.resize(170, 55)
        # btn_next.clicked.connect(uimovenext)
        #
        # return main

    def movenext(self):
        self.right_widget.setCurrentIndex(self.right_widget.currentIndex() + 1)

    def moveprevious(self):
        self.right_widget.setCurrentIndex(self.right_widget.currentIndex() - 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DesignClass()
    ex.show()
    sys.exit(app.exec_())