from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os
from summary_widget import *

class summary_display(QMainWindow):
    def __init__(self, parent=None):
        super(summary_display, self).__init__(None)
        if getattr(sys, 'frozen', None):
            self.basedir = sys._MEIPASS + "\\resources\\"
        else:
            self.basedir = os.path.dirname("resources/")
        self.summaryDisplay([0, 0, 0])
        self.move(50, 50)
        #TODO -- remove the tray bar at the bottom for the window
        self.minimizeAction = QAction(u'Minimize', self)
        self.connect(self.minimizeAction, SIGNAL("triggered()"), self.minimizeWindow)
        self.addAction(self.minimizeAction)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

        row = QHBoxLayout()

        row.addWidget(self.summaryWgt)
        row.setSpacing(0)
        centerWgt = QWidget()
        centerWgt.setLayout(row)
        centerWgt.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        #w=iconButton.width()+self.sumCrit.width()+self.sumErr.width()+self.sumWarn.width()
        w = 275
        self.setFixedSize(w, 50)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)

        self.setCentralWidget(centerWgt)
        self.setStyleSheet("background:transparent;")
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setStyleSheet(" color: black")


    def setData(self, severity):
        self.summaryWgt.updateCount(severity)


    ########
    ##Summary Display
    ########
    def summaryDisplay(self, severity):
        #set's display options for each summary label
        self.summaryWgt = QWidget()
        self.summaryWgt = summary_widget(severity, True)


    def minimizeWindow(self):
        self.hide()


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.pos()
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos().x() - self.drag_position.x(), event.globalPos().y() - self.drag_position.y())
            event.accept()

    mouseEnterEvent = pyqtSignal()
    mouseOutEvent = pyqtSignal()

    def enterEvent(self, event):
        self.mouseEnterEvent.emit()

    def leaveEvent(self, event):
        self.mouseOutEvent.emit()