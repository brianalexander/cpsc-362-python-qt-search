from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QFile, QFileInfo, QDir, QDirIterator
from PyQt5.QtWidgets import QTreeWidgetItem, QApplication
import os
import time

from tika import parser


class SearchWorker(QObject):
    def __init__(self):
        super(SearchWorker, self).__init__()
        self.qtwItems = []

    finished = pyqtSignal()
    match_found = pyqtSignal(QTreeWidgetItem, name="matchFound")

    @pyqtSlot(name="stopSearch")
    def stop_search(self):
        print('stop_search called')
        self.keep_searching = False

    @pyqtSlot(str, str, name="startSearch")
    def start_search(self, query, search_directory):
        self.keep_searching = True
        print("search started..", query)
        filters = QDir.Files

        nameFilters = ["*.cpp", "*.txt", "*.docx",
                       "*.xlsx", "*.xls", ".ppt", ".pptx", ".pdf"]

        iterator = QDirIterator(search_directory, nameFilters,
                                filters, QDirIterator.Subdirectories)
        while(iterator.hasNext()):
            QApplication.processEvents()
            if(self.keep_searching):
                filePath = iterator.next()
                if (os.access(filePath, os.R_OK)):
                    fileInfo = QFileInfo(filePath)

                    # print("opening", filePath)

                    fileContents = parser.from_file(filePath)
                    if(fileContents['status'] == 200):
                        # print("opened", type(filePath))
                        found_index = fileContents['content'].find(query)
                        if(found_index != -1):
                            snippet = fileContents['content'].strip().replace(
                                '\n', ' ').replace('\r', '')
                            snippet_index = snippet.find(query)

                            qtwItem = QTreeWidgetItem()
                            qtwItem.setText(0, fileInfo.fileName())
                            qtwItem.setText(1, fileInfo.suffix())
                            qtwItem.setText(2, str(fileInfo.size()/1024))
                            qtwItem.setText(
                                3, fileInfo.lastModified().toString("MM/dd/yyyy"))
                            qtwItem.setText(
                                4, fileInfo.created().toString("MM/dd/yyyy"))
                            qtwItem.setText(
                                5, str(snippet)[snippet_index-5:snippet_index+10])
                            qtwItem.setText(6, filePath)
                            self.qtwItems.append(qtwItem)

                            self.match_found.emit(qtwItem)
        self.finished.emit()
