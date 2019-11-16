import sys
import qdarkstyle
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QLabel, QMessageBox
from PyQt5.QtCore import QFile, QTextStream, QThread, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtGui import QPixmap, QIcon
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

        self.lightIcon = QIcon('light_button.png')
        self.ui.toggle_theme_button.setIcon(self.lightIcon)
        self.ui.toggle_theme_button.setIconSize(QSize(32,32))

        self.darkIcon = QIcon('dark_button.png')
        
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

        f = QFile("light-theme.qss")
        f.open(QFile.ReadOnly | QFile.Text)
        ts = QTextStream(f)
        self.lightqss = ts.readAll()

        self.ui.toggle_theme_button.clicked.connect(self.toggleTheme)

        self.start_search.connect(self.worker.startSearch)
        self.worker.match_found.connect(self.onMatchFound)
        self.worker.finished.connect(self.searchFinished)

        self.ui.results_tree_widget.itemDoubleClicked.connect(
            self.itemSelected)

        self.searching = False
        self.darkTheme = False


    def toggleTheme(self):
        if(self.darkTheme == False):
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
            self.ui.toggle_theme_button.setIcon(self.darkIcon)
            self.darkTheme = True
        else:
            self.setStyleSheet("") # this is the stylesheet i was planning on using: self.lightqss
            self.ui.toggle_theme_button.setIcon(self.lightIcon)
            self.darkTheme = False
        return


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
