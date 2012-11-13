__author__ = 'c0stos3'

from menu_display import *
from small_display import *
from zenoss_app import *
from zenoss_actions import *
from menu_display import *
from icon_tray import *

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import (QApplication)
import webbrowser
import Actions
from zen_threads import *
from GUI import *

from Conf import *

conf = Conf()
server = conf.server

gui = QtGui.QApplication.processEvents


class MultiWindows(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MultiWindows, self).__init__(None)
        self.__windows = []
        self.zen_get = zenoss_actions(Server=server)


    def addwindow(self, window, number):
        #self.__windows.append(window)
        if number == 1:
            self.mainwindow = window
            self.mainwindow.refreshSignal.connect(self.refreshZenData)
            self.mainwindow.summDisplay.connect(self.showSumwindow)
            self.mainwindow.openSettings.connect(self.showSettings)
            self.mainwindow.tableWidget.openMonitor.connect(self.showMonitor)
        elif number == 2:
            self.smallwindow = window
        elif number == 3:
            self.settings = window

    def display(self):
        self.mainwindow.show()
        self.smallwindow.show()
        self.refreshData()


    def refreshData(self):
        #pull new events from zenoss

        self.events = self.zen_get.getEvents()
        self.summevents = self.zen_get.summaryEvents(self.events)
        self.smallwindow.setData(self.summevents)
        self.mainwindow.refreshClick(self.events)

    def showMonitor(self):
        #TODO -- get config data and create the correct server to open
        webbrowser.open('http://10.188.106.27:8080/zport/dmd/Events/evconsole')
        pass

    def refreshZenData(self):
        self.refreshData()

    def showSumwindow(self):
        self.smallwindow.show()

    def showSettings(self):
        self.settings.show()

    def startThreads(self):
        self.threadObj = QObject()
        self.refreshThread = refresh_Thread()
        self.threadObj.moveToThread(self.refreshThread)
        self.refreshThread.start()
        self.connect(self.refreshThread, SIGNAL("refreshData()"), self.refreshData)

app = QtGui.QApplication(sys.argv)

windows = MultiWindows()
#if conf.unconfigured == True:
#windows.addwindow(Settings(servers=servers, conf=conf).show(),0)
zenoss_window = zenoss_window()
small_window = summary_display()
setting_window = settings_display(Server=conf.server)

windows.addwindow(zenoss_window, 1)
windows.addwindow(small_window, 2)
windows.addwindow(setting_window, 3)

windows.startThreads()

windows.display()
app.exec_()





