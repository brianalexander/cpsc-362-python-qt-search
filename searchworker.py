from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QFile, QFileInfo, QDir, QDirIterator
from PyQt5.QtWidgets import QTreeWidgetItem, QApplication
import os
import time

from tika import parser


class SearchWorker(QObject):
    finished = pyqtSignal()
    match_found = pyqtSignal(QTreeWidgetItem, name="matchFound")

    def __init__(self):
        super(SearchWorker, self).__init__()
        self.qtw_items = []

    @pyqtSlot(name="stopSearch")
    def stop_search(self):
        print('stop_search called')
        self.keep_searching = False

    @pyqtSlot(str, str, name="startSearch")
    def start_search(self, query, search_directory):
        self.keep_searching = True
        print("search started..", query)
        filters = QDir.Files

        nameFilters = ["*.cpp", "*.txt", "*.pdf",
                       "*.doc", "*.docx",
                       "*.xlsx", "*.xls",
                       "*.ppt", "*.pptx"]

        iterator = QDirIterator(search_directory, nameFilters,
                                filters, QDirIterator.Subdirectories)
        while(iterator.hasNext()):
            QApplication.processEvents()
            if(self.keep_searching):
                file_path = iterator.next()
                if (os.access(file_path, os.R_OK)):
                    file_info = QFileInfo(file_path)
                    file_contents = parser.from_file(file_path)

                    if(file_contents['status'] == 200 and 'content' in file_contents.keys() and file_contents['content'] is not None):
                        found_index = file_contents['content'].find(query)
                        if(found_index != -1):
                            snippet = file_contents['content'].strip().replace(
                                '\n', ' ').replace('\r', '')
                            snippet_index = snippet.find(query)

                            qtw_item = QTreeWidgetItem()
                            qtw_item.setText(0, file_info.fileName())
                            qtw_item.setText(1, file_info.suffix())
                            qtw_item.setText(2, str(file_info.size()/1024))
                            qtw_item.setText(
                                3, file_info.lastModified().toString("MM/dd/yyyy"))
                            qtw_item.setText(
                                4, file_info.created().toString("MM/dd/yyyy"))
                            qtw_item.setText(
                                5, str(snippet)[snippet_index-5:snippet_index+10])
                            qtw_item.setText(6, file_path)
                            self.qtw_items.append(qtw_item)

                            self.match_found.emit(qtw_item)
        self.finished.emit()
