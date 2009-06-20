from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QWizard, QWizardPage, QToolBar, QFileDialog, QPushButton, QTableView, QFont, QVBoxLayout
from PyQt4.QtCore import QString, QAbstractTableModel, QVariant, Qt
from camelot.view import art
from camelot.view.art import Icon
from camelot.action import createAction, addActions
from camelot.view.elixir_admin import EntityAdmin
from camelot.view.model_thread import get_model_thread
from camelot.view.controls.exception import model_thread_exception_message_box
import csv, itertools

_ = lambda x: x

class ImportWizard(QtGui.QWizard):
    """Import wizard GUI"""       
 
    def start(self):
        self.qWizard = QWizard()
        self.qWizard.setEnabled(True)
        self.qPage = QWizardPage(self.qWizard)
        self.qPage.setTitle(QString('import wizard'))
        
        self.makeButtonToSearchFile()
        
        #make grid
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.openToolBar, 1, 0)
        self.label = QtGui.QLabel('', self.qPage)
        self.grid.addWidget(self.label, 1, 1)
        
        #add layout to page
        self.qPage.setLayout(self.grid)
        self.qWizard.addPage(self.qPage)
        #make the page that shows the table
        self.qTablePage = QWizardPage(self.qWizard)
        self.qTablePage.setTitle(QString('Data from file'))
        self.qWizard.addPage(self.qTablePage)
        
        cancelButton = QPushButton(QString('cancel'), self.qWizard)
        self.qWizard.setButton(QWizard.CancelButton, cancelButton)
        
        self.finishButton = QWizard.FinishButton
        self.qWizard.setButtonText(self.finishButton, QString('finish'))
        
        self.qWizard.show()
        self.qWizard.exec_()
    
    def makeButtonToSearchFile(self):
        self.openToolBar = QToolBar(self.qPage)
        icon_file_open = Icon('tango/32x32/actions/fileopen.png').fullpath()
        self.openAct = QtGui.QAction(QtGui.QIcon(icon_file_open), 'Open File', self.openToolBar)
        self.openToolBar.connect(self.openAct, QtCore.SIGNAL('triggered()'), self.showOpenFileDialog)
        self.openToolBar.addAction(self.openAct)
               
        
    def showOpenFileDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(None, 'Open file', '/')
        self.label = QtGui.QLabel(filename, self.qPage)
        self.grid.addWidget(self.label, 2, 0)
        file=open(filename)
        self.csvreader = csv.reader(file)
        tableView = self.makeTable()
        layout = QVBoxLayout()
        layout.addWidget(tableView) 
        self.qTablePage.setLayout(layout) 
        
    def makeTable(self):
        # create the view
        tv = QTableView()

        # set the table model
        header = ['naam', 'voornaam', 'rijksregisternr', 'geslacht']
        tm = InputTableModel(self.csvreader, header, parent=self.qTablePage) 
        tv.setModel(tm)

        # set the minimum size
        self.setMinimumSize(400, 300)

        # hide grid
        tv.setShowGrid(True)

        # set the font
        font = QFont("Courier New", 20)
        tv.setFont(font)

        # hide vertical header
        vh = tv.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        tv.resizeColumnsToContents()

        # set row height
        nrows = len(list(self.csvreader))
        for row in xrange(nrows):
            tv.setRowHeight(row, 18)

        return tv
        
class InputTableModel(QAbstractTableModel): 
    def __init__(self, datain, headerdata, parent=None, *args): 
        QAbstractTableModel.__init__(self, parent, *args) 
        self.arraydata = list(datain)
        self.headerdata = headerdata
 
    def rowCount(self, parent): 
        return len(self.arraydata) 
 
    def columnCount(self, parent): 
        return len(self.arraydata[0]) 
 
    def data(self, index, role): 
        if not index.isValid(): 
            return QVariant() 
        elif role != Qt.DisplayRole: 
            return QVariant() 
        return QVariant(self.arraydata[index.row()][index.column()]) 

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()
        