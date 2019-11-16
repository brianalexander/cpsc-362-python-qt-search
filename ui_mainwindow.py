# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!

import sys
import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1126, 879)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.launch_logo = QtWidgets.QLabel(self.page)
        self.launch_logo.setAlignment(QtCore.Qt.AlignCenter)
        self.launch_logo.setObjectName("launch_logo")
        self.verticalLayout_3.addWidget(self.launch_logo)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.launch_search_box = QtWidgets.QLineEdit(self.page)
        self.launch_search_box.setObjectName("launch_search_box")
        self.horizontalLayout.addWidget(self.launch_search_box)
        self.launch_search_button = QtWidgets.QPushButton(self.page)
        self.launch_search_button.setObjectName("launch_search_button")
        self.horizontalLayout.addWidget(self.launch_search_button)

        self.toggle_theme_button = QtWidgets.QPushButton(self.page)
        self.toggle_theme_button.setObjectName("toggle_theme_button")
        self.verticalLayout.addWidget(self.toggle_theme_button, alignment=QtCore.Qt.AlignRight)
        
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.results_search_box = QtWidgets.QLineEdit(self.page_2)
        self.results_search_box.setObjectName("results_search_box")
        self.horizontalLayout_2.addWidget(self.results_search_box)
        self.results_search_button = QtWidgets.QPushButton(self.page_2)
        self.results_search_button.setObjectName("results_search_button")
        self.horizontalLayout_2.addWidget(self.results_search_button)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.results_tree_widget = QtWidgets.QTreeWidget(self.page_2)
        self.results_tree_widget.setObjectName("results_tree_widget")
        self.verticalLayout_4.addWidget(self.results_tree_widget)
        self.stackedWidget.addWidget(self.page_2)
        self.verticalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        # self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 1126, 20))
        # self.menubar.setObjectName("menubar")
        # MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)
        # self.toolBar = QtWidgets.QToolBar(MainWindow)
        # self.toolBar.setObjectName("toolBar")
        # MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.launch_logo.setText(_translate("MainWindow", "LOGO PLACEHOLDER"))

        #self.toggle_theme_button.setText(_translate("MainWindow", "Theme"))

        self.launch_search_button.setText(_translate("MainWindow", "Search"))
        self.results_search_button.setText(_translate("MainWindow", "Searching.."))
        self.results_tree_widget.headerItem().setText(0, _translate("MainWindow", "Name"))
        self.results_tree_widget.headerItem().setText(1, _translate("MainWindow", "Type"))
        self.results_tree_widget.headerItem().setText(2, _translate("MainWindow", "Size (KB)"))
        self.results_tree_widget.headerItem().setText(3, _translate("MainWindow", "Last Modified"))
        self.results_tree_widget.headerItem().setText(4, _translate("MainWindow", "Created"))
        self.results_tree_widget.headerItem().setText(5, _translate("MainWindow", "File Context"))
        self.results_tree_widget.headerItem().setText(6, _translate("MainWindow", "Path"))
        # self.toolBar.setWindowTitle(_translate("Searchy", "toolBar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
