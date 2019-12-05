from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QFile, QFileInfo, QDir, QDirIterator
from PyQt5.QtWidgets import QTreeWidgetItem
import os

from tika import parser


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

        nameFilters = ["*.cpp", "*.txt", "*.docx",
                       "*.xlsx", "*.xls", ".ppt", ".pptx", ".pdf"]  # EXCEL
        iterator = QDirIterator("/", nameFilters,
                                filters, QDirIterator.Subdirectories)
        while(iterator.hasNext()):
            filePath = iterator.next()
            if (os.access(filePath, os.R_OK)):
                fileInfo = QFileInfo(filePath)

                print("opening", filePath)

                fileContents = parser.from_file(filePath)
                if(fileContents['status'] == 200):
                    print("opened", type(filePath))
                    if(fileContents['content'].find(query) != -1):

                        qtwItem = QTreeWidgetItem()
                        qtwItem.setText(0, fileInfo.fileName())
                        qtwItem.setText(1, fileInfo.suffix())
                        qtwItem.setText(2, str(fileInfo.size()/1024))
                        qtwItem.setText(
                            3, fileInfo.lastModified().toString("MM/dd/yyyy"))
                        qtwItem.setText(
                            4, fileInfo.created().toString("MM/dd/yyyy"))
                        qtwItem.setText(
                            5, str(fileContents['content'].strip())[0:10])
                        qtwItem.setText(6, filePath)
                        self.qtwItems.append(qtwItem)

                        self.match_found.emit(qtwItem)
        print('finished')

        self.finished.emit()
