from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QFile, QFileInfo, QDir, QDirIterator
from PyQt5.QtWidgets import QTreeWidgetItem

#.doc OR .docx -> txt
import docx2txt

#.xlsl -> txt
import xlrd

def extractTextXL(filePath):
    arr = []
    wkbk = xlrd.open_workbook(filePath, on_demand = True)
    for nsheet in range(wkbk.nsheets):
        sheet = wkbk.sheet_by_index(nsheet)
        for row in range(sheet.nrows):
            for col in range(sheet.ncols):
                if sheet.cell(row, col).value != xlrd.empty_cell.value:
                    arr.append(sheet.cell(row, col).value)
                arr.append("\t")
            arr.append("\n")
    fileContents = ""
    return fileContents.join(arr)
 


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
        nameFilters = ["*.cpp", "*.txt", "*.doc", "*.docx", "*.xlsx", "*.xls"]
        iterator = QDirIterator("/Users", nameFilters,
                                filters, QDirIterator.Subdirectories)
        while(iterator.hasNext()):
            filePath = iterator.next()
            fileInfo = QFileInfo(filePath)
            currentFile = QFile(filePath)
            currentFile.open(QFile.ReadOnly | QFile.Text)
            fileContents = ""
            # fileContents = currentFile.readAll().data().decode('utf8', errors='ignore')
            
            if(filePath.endswith(".xlsx") | filePath.endswith(".xls")): #XLS or XLSX
                fileContents = extractTextXL(filePath)
            elif(filePath.endswith(".cpp") | filePath.endswith(".txt") | filePath.endswith(".h")):    #CPP or H or TXT 
                fileContents = currentFile.readAll().data().decode('utf8', errors='ignore')
            elif(filePath.endswith(".doc") | filePath.endswith(".docx")):   #DOC or DOCX
                fileContents = docx2txt.process(filePath)
                
            if(fileContents.find(query) != -1):
                qtwItem = QTreeWidgetItem()
                qtwItem.setText(0, fileInfo.fileName())
                qtwItem.setText(1, fileInfo.suffix())
                qtwItem.setText(2, str(fileInfo.size()/1024))
                qtwItem.setText(3, fileInfo.lastModified().toString("MM/dd/yyyy"))
                qtwItem.setText(4, fileInfo.created().toString("MM/dd/yyyy"))
                qtwItem.setText(5, str(fileContents[0:50]))
                qtwItem.setText(6, filePath)
                self.qtwItems.append(qtwItem)

                self.match_found.emit(qtwItem)

        self.finished.emit()
