import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QLabel, QMessageBox
from PyQt5.QtCore import QFile, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from ui_mainwindow import Ui_MainWindow
from searchworker import SearchWorker
from filecontentview import FileContentView


class MainWindow(QMainWindow):

    start_search = pyqtSignal(str, name='startSearch')

    def __init__(self):
        super(MainWindow, self).__init__()
        self.openedFiles = []

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        logo = QPixmap('searchy_logo.png')
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

        self.start_search.connect(self.worker.startSearch)
        self.worker.match_found.connect(self.onMatchFound)
        self.worker.finished.connect(self.searchFinished)

        self.ui.results_tree_widget.itemDoubleClicked.connect(
            self.itemSelected)

        self.searching = False

    def searchButtonClicked(self):
        if(self.searching == True):
            return

        self.searching = True

        if(self.ui.stackedWidget.currentIndex() == 1):
            self.ui.results_tree_widget.clear()
            self.currentQuery = self.ui.results_search_box.text()
            self.ui.results_search_button.setText('Searching..')
        else:
            self.ui.results_search_box.setText(
                self.ui.launch_search_box.text())
            self.currentQuery = self.ui.launch_search_box.text()
            self.ui.stackedWidget.setCurrentIndex(1)

        self.start_search.emit(self.currentQuery)

    @pyqtSlot(QTreeWidgetItem)
    def onMatchFound(self, qtwItem):
        self.ui.results_tree_widget.addTopLevelItem(qtwItem)

    @pyqtSlot(QTreeWidgetItem, int)
    def itemSelected(self, item, column):
        f = QFile(item.text(6))
        f.open(QFile.ReadOnly | QFile.Text)
        fileContentString = f.readAll().data().decode('utf8', errors='ignore')
        f.close()

        fileContentView = FileContentView()
        fileContentView.openHighlightedDocument(
            fileContentString, self.currentQuery)
        self.openedFiles.append(fileContentView)
        fileContentView.show()

    @pyqtSlot()
    def searchFinished(self):
        self.ui.results_search_button.setText("Search")
        self.searching = False
        if(self.ui.results_tree_widget.topLevelItemCount() == 0):
            QMessageBox.information(self, "Searchy", "No results found.")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
