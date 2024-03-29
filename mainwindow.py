from filecontentview import FileContentView
from searchworker import SearchWorker
from ui_mainwindow import Ui_MainWindow
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor
from PyQt5.QtCore import Qt, QFile, QThread, pyqtSignal, pyqtSlot, QSize, QTextStream
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QLabel, QMessageBox, QFileDialog, QSplashScreen
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
        self.dark_theme = False

        self.light_icon = QIcon(':assets/icons/light_button.png')
        self.dark_icon = QIcon(':assets/icons/dark_button.png')

        self.ui.toggle_theme_button.setIcon(self.dark_icon)
        self.ui.toggle_theme_button.setIconSize(QSize(32, 32))

        self.opened_files = []

        logo = QPixmap(':/assets/images/searchy_logo.png')
        self.ui.launch_logo.setPixmap(logo)

        self.worker_thread = QThread()
        self.worker_thread.start()

        self.worker = SearchWorker()
        self.worker.moveToThread(self.worker_thread)

        self.ui.launch_search_button.clicked.connect(
            self.search_button_clicked)
        self.ui.launch_search_box.returnPressed.connect(
            self.search_button_clicked)

        self.ui.results_search_button.clicked.connect(
            self.search_button_clicked)
        self.ui.results_search_box.returnPressed.connect(
            self.search_button_clicked)

        self.ui.toggle_theme_button.clicked.connect(self.toggle_theme)

        self.ui.launch_directory_button.clicked.connect(self.choose_directory)

        self.start_search.connect(self.worker.start_search)
        self.stop_search.connect(self.worker.stop_search)
        self.worker.match_found.connect(self.on_match_found)
        self.worker.finished.connect(self.search_finished)

        self.ui.results_tree_widget.itemDoubleClicked.connect(
            self.item_selected)

        self.searching = False

    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Open Directory",
            os.path.abspath(os.sep),
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )

        self.search_directory = directory

    def toggle_theme(self):
        if(self.dark_theme == False):
            self.application_context.setStyleSheet(
                qdarkstyle.load_stylesheet_pyqt5())
            self.ui.toggle_theme_button.setIcon(self.light_icon)
            self.dark_theme = True
        else:
            self.application_context.setStyleSheet("")
            self.ui.toggle_theme_button.setIcon(self.dark_icon)
            self.dark_theme = False

    def search_button_clicked(self):
        if (self.searching == True):
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
    def on_match_found(self, qtwItem):
        self.ui.results_tree_widget.addTopLevelItem(qtwItem)

    @pyqtSlot(QTreeWidgetItem, int)
    def item_selected(self, item, column):
        file_content = parser.from_file(item.text(6))['content'].strip()

        file_content_view = FileContentView()
        file_content_view.open_highlighted_document(
            file_content, self.current_query)
        self.opened_files.append(file_content_view)
        file_content_view.show()

    @pyqtSlot()
    def search_finished(self):
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
    image = QPixmap(':/assets/images/searchy_logo.png')

    background = QPixmap(image.size())
    background.fill(QColor("black"))

    painter = QPainter(background)
    painter.drawPixmap(0,0, image)


    splash = QSplashScreen(background)
    splash.show()
    # QMessageBox.information(None, "Searchy", "No results found.")

    # dummy call to start VM on startup
    parser.from_buffer('')

    window = MainWindow(app)
    window.show()

    splash.finish(window)

    sys.exit(app.exec_())
