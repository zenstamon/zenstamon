__author__ = 'c0stos3'
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ast
from PyQt4.QtCore import (QThread, pyqtSignal)

class event_widget(QTableWidget):
    def __init__(self, parent=None):
        super(event_widget, self).__init__(parent)
        #self.tableWidget = QTableWidget()

        self.evtColCount = 7

        self.setColumnCount(self.evtColCount)
        self.setRowCount(0)
        #item = QTableWidgetItem()
        #self.setHorizontalHeaderItem(0, item)
        #item = QTableWidgetItem()
        #self.setHorizontalHeaderItem(1, item)
        #item = QTableWidgetItem()
        #self.setHorizontalHeaderItem(2, item)

        for i in range(self.evtColCount):
            item = QTableWidgetItem()
            self.setHorizontalHeaderItem(i, item)

        self.setHorizontalHeaderItem(0, QTableWidgetItem("Host"))
        self.setHorizontalHeaderItem(1, QTableWidgetItem("Status"))
        self.setHorizontalHeaderItem(2, QTableWidgetItem("Message"))
        self.setHorizontalHeaderItem(3, QTableWidgetItem("Event Class"))
        self.setHorizontalHeaderItem(4, QTableWidgetItem("Count"))
        self.setHorizontalHeaderItem(5, QTableWidgetItem("First Seen"))
        self.setHorizontalHeaderItem(6, QTableWidgetItem("Last Seen"))

        self.horizontalHeader().setResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)

        self.horizontalHeader().setClickable(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.action_monitor = QAction(u'Monitor', self)
        self.action_accept = QAction(u'Accept', self)
        self.action_delete = QAction(u'Delete', self)

        self.connect(self, SIGNAL("cellClicked(int, int)"), self.cellClick)
        self.connect(self.action_monitor, SIGNAL("triggered()"), self.menuMonitor)
        self.connect(self.action_accept, SIGNAL("triggered()"), self.menuAccept)
        self.connect(self.action_delete, SIGNAL("triggered()"), self.menuDelete)

        self.setMouseTracking(True)

        self.addAction(self.action_monitor)
        separator = QAction(self)
        separator.setSeparator(True)
        self.addAction(separator)
        self.addAction(self.action_accept)
        self.addAction(self.action_delete)
        self.repaint()
        self.action_accept.setDisabled(True)
        self.action_delete.setDisabled(False)

        self.previousColor = QColor("yellow")
        self.previousRow = 0
        self.isFirstHover = True


    openMonitor = pyqtSignal()


    def menuMonitor(self):
        #print(str(self.setX),str(self.setY)+" -- menuAccept clicked")
        self.openMonitor.emit()
        pass

    def menuAccept(self):
        #TODO -- connect with api
        #print(str(self.setX),str(self.setY)+" -- menuAccept clicked")
        pass

    def menuDelete(self):
        #TODO -- connect with api
        #print(str(self.setX),str(self.setY)+" -- menuAccept clicked")
        #print(self.setX)
        #print("click")
        self.emit(SIGNAL("deleteEvent(PyQt_PyObject)"), self.setX)

        pass

    def cellClick(self, x, y):
        #print(str(x),str(y))
        self.setX = x
        self.setY = y

    def setColHidden(self, Conf):
        self.setColumnHidden(0, not ast.literal_eval(Conf.eventConf.host))
        self.setColumnHidden(1, not ast.literal_eval(Conf.eventConf.state))
        self.setColumnHidden(2, not ast.literal_eval(Conf.eventConf.message))
        self.setColumnHidden(3, not ast.literal_eval(Conf.eventConf.eventclass))
        self.setColumnHidden(4, not ast.literal_eval(Conf.eventConf.count))
        self.setColumnHidden(5, not ast.literal_eval(Conf.eventConf.first))
        self.setColumnHidden(6, not ast.literal_eval(Conf.eventConf.last))

        pass

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        print("Mouse Event")
        Action = menu.addAction("I am a " + self.name + " Action")
        Action.triggered.connect(self.printName)

        menu.exec_(event.globalPos())

    def mouseMoveEvent(self, event):
        #TODO -- need to make it cleaner so if you scoll off the page the highlight goes away
        #TODO -- Bug: when an event is removed and then the events update, the removed event has the last color, not what is currenctly at there before.
        try:
            for y in range(self.columnCount()):
                if self.isFirstHover == False:
                    self.item(self.previousRow, y).setBackgroundColor(self.previousColor)

            self.previousColor = self.item(self.itemAt(event.pos()).row(), 0).backgroundColor()

            for y in range(self.columnCount()):
                self.item(self.itemAt(event.pos()).row(), y).setBackgroundColor(QColor("lightgray"))

            self.previousRow = self.itemAt(event.pos()).row()
            self.isFirstHover = False
        except:
            pass
            #print(self.OnItem)

    def cellClicked(self, x, y):
        print("zxcv")

    def itemClicked(self, event):
        print("qwer")

    def clicked(self, event):
        print("asdf")

    def leaveEvent(self, event):
        #######
        ###TODO -- need to make it cleaner so if you scoll off the page the highlight goes away
        #######
        for y in range(self.columnCount()):
            if self.isFirstHover == False:
                self.item(self.previousRow, y).setBackgroundColor(self.previousColor)
                pass
        self.isFirstHover = True
