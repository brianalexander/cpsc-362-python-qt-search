import sys
from PyQt5.QtWidgets import QWidget
from ui_filecontentview import Ui_FileContentView

class FileContentView(QWidget):
    def __init__(self):
        super(FileContentView, self).__init__()

        self.ui = Ui_FileContentView()
        self.ui.setupUi(self)

    def setText(self, fileContent):
        self.ui.popup_text_box.setText(fileContent)