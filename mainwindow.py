from filecontentview import FileContentView
from searchworker import SearchWorker
from ui_mainwindow import Ui_MainWindow
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QFile, QThread, pyqtSignal, pyqtSlot, QSize, QTextStream
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QLabel, QMessageBox, QFileDialog
import os
import resources
import qdarkstyle
import sys


class MainWindow(QMainWindow):

    start_search = pyqtSignal(str, str, name='startSearch')
    stop_search = pyqtSignal()

    def __init__(self, application_context):
        super(MainWindow, self).__init__()
        self.application_context = application_context

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.search_directory = os.path.abspath(os.sep)

        # self.application_context.setStyleSheet(
        #     qdarkstyle.load_stylesheet_pyqt5())
        self.darkTheme = False

        self.lightIcon = QIcon(':assets/icons/light_button.png')
        self.darkIcon = QIcon(':assets/icons/dark_button.png')

        self.ui.toggle_theme_button.setIcon(self.darkIcon)
        self.ui.toggle_theme_button.setIconSize(QSize(32, 32))

        self.openedFiles = []

        logo = QPixmap(':/assets/images/searchy_logo.png')
        self.ui.launch_logo.setPixmap(logo)

        self.workerThread = QThread()
        self.workerThread.start()

        self.worker = SearchWorker()
        self.worker.moveToThread(self.workerThread)

        self.ui.launch_search_button.clicked.connect(self.searchButtonClicked)
        self.ui.launch_search_box.returnPressed.connect(
            self.searchButtonClicked)

        self.ui.results_search_button.clicked.connect(self.searchButtonClicked)
        self.ui.results_search_box.returnPressed.connect(
            self.searchButtonClicked)

        self.ui.toggle_theme_button.clicked.connect(self.toggleTheme)

        self.ui.launch_directory_button.clicked.connect(self.choose_directory)

        self.start_search.connect(self.worker.start_search)
        self.stop_search.connect(self.worker.stop_search)
        self.worker.match_found.connect(self.onMatchFound)
        self.worker.finished.connect(self.searchFinished)

        self.ui.results_tree_widget.itemDoubleClicked.connect(
            self.itemSelected)

        self.searching = False

    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Open Directory",
            os.path.abspath(os.sep),
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )

        self.search_directory = directory

    def toggleTheme(self):
        if(self.darkTheme == False):
            self.application_context.setStyleSheet(
                qdarkstyle.load_stylesheet_pyqt5())
            self.ui.toggle_theme_button.setIcon(self.lightIcon)
            self.darkTheme = True
        else:
            self.application_context.setStyleSheet("")
            self.ui.toggle_theme_button.setIcon(self.darkIcon)
            self.darkTheme = False

    def searchButtonClicked(self):
        if (self.searching == True):
            print('emitting stop_search')
            self.stop_search.emit()
            self.searching = False
            self.ui.results_search_button.setText('Search')

        else:
            self.searching = True

            if(self.ui.stackedWidget.currentIndex() == 1):
                self.ui.results_tree_widget.clear()
                self.current_query = self.ui.results_search_box.text()
                self.ui.results_search_button.setText('Searching..')
            else:
                self.ui.results_search_box.setText(
                    self.ui.launch_search_box.text())
                self.current_query = self.ui.launch_search_box.text()
                self.ui.stackedWidget.setCurrentIndex(1)

            self.start_search.emit(self.current_query, self.search_directory)

    @pyqtSlot(QTreeWidgetItem)
    def onMatchFound(self, qtwItem):
        self.ui.results_tree_widget.addTopLevelItem(qtwItem)

    @pyqtSlot(QTreeWidgetItem, int)
    def itemSelected(self, item, column):
        fileContent = parser.from_file(item.text(6))['content'].strip()

        fileContentView = FileContentView()
        fileContentView.openHighlightedDocument(
            fileContent, self.current_query)
        self.openedFiles.append(fileContentView)
        fileContentView.show()

    @pyqtSlot()
    def searchFinished(self):
        self.ui.results_search_button.setText("Search")
        self.searching = False
        if(self.ui.results_tree_widget.topLevelItemCount() == 0):
            QMessageBox.information(self, "Searchy", "No results found.")
        else:
            QMessageBox.information(self, "Searchy", "Finished searching!")


if __name__ == "__main__":
    import tika
    from tika import parser

    app = QApplication(sys.argv)

    # dummy call to start VM on startup
    parser.from_buffer('')

    window = MainWindow(app)
    window.show()

    sys.exit(app.exec_())
