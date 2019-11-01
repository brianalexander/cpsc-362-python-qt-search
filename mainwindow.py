import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem
from PyQt5.QtCore import QFile, QThread, pyqtSignal, pyqtSlot
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

        self.workerThread = QThread()
        self.workerThread.start()

        self.worker = SearchWorker()
        self.worker.moveToThread(self.workerThread)

        self.ui.launch_search_button.clicked.connect(self.searchButtonClicked)
        self.start_search.connect(self.worker.startSearch)
        self.worker.match_found.connect(self.onMatchFound)
        self.ui.results_tree_widget.itemDoubleClicked.connect(self.itemSelected)


    def searchButtonClicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.results_search_box.setText(self.ui.launch_search_box.text())
        
        self.start_search.emit(self.ui.launch_search_box.text())

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
        fileContentView.setText(fileContentString)
        self.openedFiles.append(fileContentView)
        fileContentView.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())