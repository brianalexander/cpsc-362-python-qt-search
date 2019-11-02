from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QFile, QFileInfo, QDir, QDirIterator
from PyQt5.QtWidgets import QTreeWidgetItem

from PyPDF2 import PdfFileReader


class SearchWorker(QObject):

    def __init__(self):
        super(SearchWorker, self).__init__()
        self.qtwItems = []

    finished = pyqtSignal()
    match_found = pyqtSignal(QTreeWidgetItem, name="matchFound")

    @pyqtSlot(str)
    def startSearch(self, query):
        print("search started..", query)
        filters = QDir.Files
        nameFilters = ["*.cpp"]
        iterator = QDirIterator("/home/alexanderb", nameFilters,
                                filters, QDirIterator.Subdirectories)
        while(iterator.hasNext()):
            filePath = iterator.next()
            fileInfo = QFileInfo(filePath)
            currentFile = QFile(filePath)
            currentFile.open(QFile.ReadOnly | QFile.Text)
            fileContents = currentFile.readAll().data().decode('utf8', errors='ignore')
            if(fileContents.find(query) != -1):
                qtwItem = QTreeWidgetItem()
                qtwItem.setText(0, fileInfo.fileName())
                qtwItem.setText(1, fileInfo.suffix())
                qtwItem.setText(2, str(fileInfo.size()/1024))
                qtwItem.setText(
                    3, fileInfo.lastModified().toString("MM/dd/yyyy"))
                qtwItem.setText(4, fileInfo.created().toString("MM/dd/yyyy"))
                qtwItem.setText(5, str("...here is the content..."))
                qtwItem.setText(6, filePath)
                self.qtwItems.append(qtwItem)

                self.match_found.emit(qtwItem)

        self.finished.emit()
