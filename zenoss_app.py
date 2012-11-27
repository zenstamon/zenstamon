__author__ = 'c0stos3'

#!/usr/bin/env python
# Copyright (c) 2008 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.



from PyQt4.QtCore import *
from PyQt4.QtGui import *

from zenoss_api import *
from icon_tray import *
from events import *
from event_widget import *
from summary_widget import *

class zenoss_window(QMainWindow):
    ########
    ##Start System Tray Icon
    ########
    def startTray(self, severity):
        self.trayIcon = SystemTrayIcon(QIcon(self.basedir + "/Zenoss_O_green.png"), self)
        self.refreshTrayIcon(severity)

    ########
    ##Top Menu Row Buttons
    ########
    def configMenuButton(self):
        refreshBtn = QPushButton()
        quitBtn = QPushButton()
        settingBtn = QPushButton()
        settingBtn.setIcon(QIcon(self.basedir + "/settings.png"))
        refreshBtn.setIcon(QIcon(self.basedir + "/recheckall.png"))
        quitBtn.setIcon(QIcon(self.basedir + "/close.png"))
        refreshBtn.setFixedSize(80, 24)
        refreshBtn.setText("Refresh")
        settingBtn.setText("Settings")
        #quitBtn.setFixedSize(30, 30)
        #quitBtn.setText("QUIT")
        refreshBtn.setStyleSheet("background-color: lightgray;")
        settingBtn.setStyleSheet("background-color: lightgray;")
        quitBtn.setStyleSheet("background-color: lightgray;")
        self.connect(quitBtn, SIGNAL("clicked()"), self.minimize)
        self.connect(settingBtn, SIGNAL("clicked()"), self.settings)

        self.connect(refreshBtn, SIGNAL("clicked()"), self.refreshBtnClick)

        iconLbl = QIcon(self.basedir + "/Zenoss_Z_green.png")
        appName = QLabel("Zenstamon")

        iconButton = QLabel()
        iconButton.setPixmap(QPixmap.fromImage(QImage(self.basedir + "/zenstamon_small.png")))
        iconButton.setAutoFillBackground(True)
        iconButton.setStyleSheet("color: green;font-size:14px;")
        appName.setStyleSheet("font-size:14px;")
        #iconButton.setFont(QFont("Arial",25, QFont.Bold ))


        menuLayout = QHBoxLayout()
        menuLayout.addWidget(iconButton)
        menuLayout.addWidget(appName)
        menuLayout.insertStretch(5)
        menuLayout.addWidget(refreshBtn)
        menuLayout.addWidget(settingBtn)
        menuLayout.addWidget(quitBtn)
        self.topWgt = QWidget()
        self.topWgt.setLayout(menuLayout)

    ########
    ##Summary Display
    ########
    def summaryDisplay(self, severity):
        self.summaryWgt = summary_widget(severity, False)

    ########
    ##Button Actions
    ########
    def minimize(self):
        self.hide()

    def displaySummWindow(self):
        self.summDisplay.emit()


    def refreshBtnClick(self):
        #need to call parent function
        self.refreshSignal.emit()

    def settings(self):
        self.openSettings.emit()

    def refreshClick(self, events):
        self.tableWidget.clearContents()
        self.reloadEvents(events)
        self.resizeApp()


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.pos()
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos().x() - self.drag_position.x(), event.globalPos().y() - self.drag_position.y())
            event.accept()


    def sortList(self, eventGrid, totalRows):
        tmp = []

        for x in range(6):
            for y in range(totalRows):
                if x == 0 and eventGrid[y].severity == "CRITICAL":
                    tmp.append(eventGrid[y])
                if x == 1 and eventGrid[y].severity == "ERROR":
                    tmp.append(eventGrid[y])
                if x == 2 and eventGrid[y].severity == "WARNING":
                    tmp.append(eventGrid[y])
                if x == 3 and eventGrid[y].severity == "INFO":
                    tmp.append(eventGrid[y])
                if x == 4 and eventGrid[y].severity == "DEBUG":
                    tmp.append(eventGrid[y])
                if x == 5 and eventGrid[y].severity == "CLEAR":
                    tmp.append(eventGrid[y])

        return tmp

    def resizeApp(self):
        height = 0
        height = height + self.topWgt.height()
        height = height + self.summaryWgt.height()
        height = height + self.eventWgt.height()
        self.setFixedHeight(height + 30)

    ########
    ## Generate Event List
    ########
    def reloadEvents(self, events):
        critical = 0
        error = 0
        warning = 0
        info = 0
        debug = 0
        clear = 0
        for e in events['events'][:]:
            if e['severity'] == 5:
                critical = critical + 1
            elif e['severity'] == 4:
                error = error + 1
            elif e['severity'] == 3:
                warning = warning + 1
            elif e['severity'] == 2:
                info = info + 1
            elif e['severity'] == 1:
                debug = debug + 1
            elif e['severity'] == 0:
                clear = clear + 1
        totalRows = critical + error + warning + info
        severity = []
        severity.append(critical)
        severity.append(error)
        severity.append(warning)
        severity.append(info)
        severity.append(debug)
        severity.append(clear)

        eventLayout = QVBoxLayout()
        eventGrid = []
        for e in events['events'][:]:
            eventGrid.append(Event(e['device']['text'] + '\t',
                e['severity'], e['message'], e['evid'], e['firstTime'], e['lastTime'], e['count'],
                e['eventClass']['text'], e['component']['text']))

        eventGrid = self.sortList(eventGrid, totalRows)

        self.setlistEvents(eventGrid, totalRows)
        self.refreshSummary(severity)
        self.refreshTrayIcon(severity)


    def refreshSummary(self, severity):
        self.summaryWgt.updateCount(severity)


    def refreshTrayIcon(self, severity):
        #TODO -- add error as option
        critical = severity[0]
        error = severity[1]
        warning = severity[2]
        play = False
        if (critical > 0):
            if self.state != critical:
                play = True
                self.state = critical
            self.trayIcon.set_icon_critical(play)
        elif error > 0:
            if self.state != error:
                play = True
                self.state = error
            self.trayIcon.set_icon_error(play)
        elif (warning > 0 ):
            if self.state != warning:
                play = True
                self.state = warning
            self.trayIcon.set_icon_warn(play)
        else:
            self.trayIcon.action_ok.trigger()
        self.trayIcon.show()

    def setlistEvents(self, eventGrid, totalRows):
        total = 0
        self.eventUID = []
        self.tableWidget.setRowCount(totalRows)
        for x in range(totalRows):
            self.tableWidget.setItem(total, 0, QTableWidgetItem(eventGrid[x].server))
            self.tableWidget.setItem(total, 1, QTableWidgetItem(eventGrid[x].severity))
            self.tableWidget.setItem(total, 2, QTableWidgetItem(eventGrid[x].message))
            self.tableWidget.setItem(total, 3, QTableWidgetItem(eventGrid[x].component))
            self.tableWidget.setItem(total, 4, QTableWidgetItem(str(eventGrid[x].count)))

            self.tableWidget.setItem(total, 5, QTableWidgetItem(eventGrid[x].firstseen))
            self.tableWidget.setItem(total, 6, QTableWidgetItem(eventGrid[x].lastseen))

            self.eventUID.append(eventGrid[x].eventid)

            if eventGrid[x].severity == "CRITICAL":
                color = "red"
                txtcolor = "white"
            elif eventGrid[x].severity == "ERROR":
                color = "orange"
                txtcolor = "black"
            elif eventGrid[x].severity == "WARNING":
                color = "yellow"
                txtcolor = "black"
            for y in range(7):
                self.tableWidget.item(x, y).setBackgroundColor(QColor(color))
                self.tableWidget.item(x, y).setTextColor(QColor(txtcolor))
                self.tableWidget.item(x, y).setFlags(Qt.NoItemFlags)

            total = total + 1

        self.tableWidget.setColumnWidth(2, 600)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.repaint()
        self.tableWidget.setColumnWidth(2, 600)
        self.tableWidget.repaint()
        h = self.tableWidget.height() + 20
        w = self.tableWidget.width() + 20
        tmpWidth = 0
        tmpHeight = 0
        for x in range(self.tableWidget.columnCount()):
            if not self.tableWidget.isColumnHidden(x):
                tmpWidth = tmpWidth + self.tableWidget.columnWidth(x)


                # print(self.tableWidget.columnWidth(x))
                #tmpWidth=tmpWidth+600
        for x in range(self.tableWidget.rowCount() + 1):
            tmpHeight = tmpHeight + self.tableWidget.rowHeight(x)
            #print(str(tmpWidth) + ", " + str(tmpHeight))
        #print(str(w)+" -- "+str(h))
        #print(str(tmpWidth+w))




        screenHeight = QDesktopWidget().availableGeometry().height()
        screenWidth = QDesktopWidget().availableGeometry().width()
        if screenHeight > tmpHeight + 30:
            self.tableWidget.setFixedSize(tmpWidth + 20, tmpHeight + 30)
        else:
            self.tableWidget.setFixedSize(tmpWidth + 20, screenHeight - 150)
            #TODO -- Not sure if we want to move the screen if the size of the app window exceeds the size of the screen.
            #self.move((screenWidth/2) -(tmpWidth/2) ,10)

        self.setFixedWidth(tmpWidth + 40)

    def initTableEvents(self):
        #self.tableWidget = QTableWidget()
        self.tableWidget = event_widget(self)
        self.eventWgt = self.tableWidget
        self.eventWgt.repaint()
        self.connect(self.tableWidget, SIGNAL("deleteEvent(PyQt_PyObject)"), self.deleteEvent)

    def setConfigSettings(self, Config):
        self.config = Config
        self.tableWidget.setColHidden(Config)


    def updateEventTable(self):
        pass

    def deleteEvent(self, row):
        eventuid = self.eventUID[row]
        self.emit(SIGNAL("deleteEvent(PyQt_PyObject)"), eventuid)
        #self.emit(SIGNAL("deleteEvent(PyQt_PyObject)"), eventuid)
        pass

    #@@@@@@@@
    ### Initialize GUI
    #@@@@@@@@
    #@@@@@@@@
    refreshSignal = pyqtSignal()
    summDisplay = pyqtSignal()
    openSettings = pyqtSignal()

    def __init__(self, parent=None):
        super(zenoss_window, self).__init__(parent)
        #remove's windows border but is not movable.
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.mainLayout = QBoxLayout(QBoxLayout.TopToBottom, )
        if getattr(sys, 'frozen', None):
            self.basedir = sys._MEIPASS + "\\resources\\"
        else:
            self.basedir = os.path.dirname("resources/")
        self.state = None
        ########
        ##Icon Tray Status
        #########
        self.startTray([0, 0, 0])
        self.trayIcon.displaySummWindow.connect(self.displaySummWindow)

        ########
        ##Top menu Bar Buttons
        #########
        self.configMenuButton()

        ########
        ##Summary Row
        ########
        self.summaryDisplay([0, 0, 0])

        ########
        ##Events
        #########
        self.initTableEvents()



        ########
        ##Main Window Settings
        ########
        self.mainLayout = QBoxLayout(QBoxLayout.TopToBottom, )
        #mainLayout.addItem(menuLayout)
        self.mainLayout.addWidget(self.topWgt)
        self.mainLayout.addWidget(self.summaryWgt)
        #self.mainLayout.addWidget(self.headerWgt)
        self.mainLayout.addWidget(self.eventWgt)
        self.centerWidget = QWidget()

        self.centerWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.centerWidget)

        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: lightgray;") #cornflowerblue
        self.setWindowIcon(QtGui.QIcon(self.basedir + '/zenstamon_small.png'))

        self.setWindowTitle("Zenstamon")


#app = QApplication(sys.argv)
#form = Form()
#form.show()
#app.exec_()

