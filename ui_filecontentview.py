# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filecontentview.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!

import sys
import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FileContentView(object):
    def setupUi(self, FileContentView):
        FileContentView.setObjectName("FileContentView")
        FileContentView.resize(651, 467)
        self.verticalLayout = QtWidgets.QVBoxLayout(FileContentView)
        self.verticalLayout.setObjectName("verticalLayout")
        self.popup_text_box = QtWidgets.QTextEdit(FileContentView)
        self.popup_text_box.setObjectName("popup_text_box")
        self.verticalLayout.addWidget(self.popup_text_box)

        self.retranslateUi(FileContentView)
        QtCore.QMetaObject.connectSlotsByName(FileContentView)
        FileContentView.show()

    def retranslateUi(self, FileContentView):
        _translate = QtCore.QCoreApplication.translate
        FileContentView.setWindowTitle(_translate("FileContentView", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FileContentView = QtWidgets.QWidget()
    ui = Ui_FileContentView()
    ui.setupUi(FileContentView)
    sys.exit(app.exec_())