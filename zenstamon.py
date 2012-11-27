from menu_display import *
from small_display import *
from zenoss_app import *
from zenoss_actions import *

import sys
import webbrowser
from zen_threads import *

gui = QtGui.QApplication.processEvents


class MultiWindows(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MultiWindows, self).__init__(None)
        self.__windows = []
        #Load Config data if it exits
        self.conf = Conf()
        self.refreshThread = None
        logging.basicConfig(filename='zenoss_log.log', level=logging.DEBUG, format='%(asctime)s %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p')
        self.smallWindisplay = False


    def checkConfig(self):
        if self.conf.unconfigured == True:
            self.displayConfig()
        else:
            self.checkConnection()
        pass

    def displayConfig(self):
        self.settings.setConfigData(self.conf)
        self.settings.show()

    def reloadConfig(self):
        self.conf = Conf()
        self.checkConfig()

    def checkConnection(self):
        logging.debug("Check Connections")
        self.zen_get = zenoss_actions(Server=self.conf.server)
        self.events = self.zen_get.getEvents()
        self.settings.setConfigData(self.conf)

        if self.events == False:
            self.mainwindow.show()
            self.smallwindow.hide()
            msgBox = QMessageBox()
            msgBox.setText("Error: Can not connect to Zenoss Server");
            self.stopThreads()
            msgBox.exec_()
            logging.debug("Connection Failed")
        else:
            logging.debug("Connected - App Started")
            self.startApp()

    def startApp(self):
        self.stopThreads()
        self.zen_get = zenoss_actions(Server=self.conf.server)
        self.connect(self.mainwindow, SIGNAL("deleteEvent(PyQt_PyObject)"), self.deleteEvent)
        self.startThreads()
        self.updateDisplayconfigs()
        self.display()

    #TODO -- not sure when the best time to update the GUI with config data
    def updateDisplayconfigs(self):
        self.mainwindow.setConfigSettings(self.conf)

        pass

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
            self.smallwindow.mouseEnterEvent.connect(self.mouseInSmWin)
            self.smallwindow.mouseOutEvent.connect(self.mouseOutSmWin)
        elif number == 3:
            self.settings = window
            self.settings.menuSaveClick.connect(self.reloadConfig)

    def display(self):
        self.mainwindow.show()
        #self.smallwindow.show()
        self.manualRefresh()


    def manualRefresh(self):
        self.events = self.zen_get.getEvents()
        self.summevents = self.zen_get.summaryEvents(self.events)
        self.smallwindow.setData(self.summevents)
        self.mainwindow.refreshClick(self.events)


    def refreshData(self, eventJson):
        #pull new events from zenoss
        #self.events = self.zen_get.getEvents()
        self.summevents = self.zen_get.summaryEvents(eventJson)
        self.smallwindow.setData(self.summevents)
        self.mainwindow.refreshClick(eventJson)


    def showMonitor(self):
        #TODO -- get config data and create the correct server to open
        webbrowser.open(
            'http://' + self.conf.server.server_url + ':' + self.conf.server.server_port + '/zport/dmd/Events/evconsole')
        pass

    def deleteEvent(self, eventUid):
        self.zen_get.deleteEvent(eventUid)
        self.manualRefresh()
        pass

    def stopThreads(self):
        #print("stop thread")
        if self.refreshThread != None:
            self.refreshThread.terminate()

    def startThreads(self):
        self.threadObj = QObject()
        self.refreshThread = refresh_Thread(server=self.conf.server, refreshTime=self.conf.eventConf.duration)#
        self.threadObj.moveToThread(self.refreshThread)
        self.refreshThread.start()
        self.connect(self.refreshThread, SIGNAL("refreshData(PyQt_PyObject)"), self.refreshData)
        #print("startThread")

    def refreshZenData(self):
        self.manualRefresh()

    def showSumwindow(self):
        self.smallwindow.show()

    def showSettings(self):
        self.settings.show()

    def mouseInSmWin(self):
        if self.mainwindow.isHidden():
            self.smallWindisplay = True
            self.mainwindow.show()
            self.mainwindow.move(self.smallwindow.x(), (self.smallwindow.y() + 35))

    def mouseOutSmWin(self):
        if self.smallWindisplay == True:
            self.mainwindow.hide()
            self.smallWindisplay = False
        pass


app = QtGui.QApplication(sys.argv)

windows = MultiWindows()

zenoss_window = zenoss_window()
small_window = summary_display()
setting_window = settings_display()

windows.addwindow(zenoss_window, 1)
windows.addwindow(small_window, 2)
windows.addwindow(setting_window, 3)
windows.checkConfig()

app.exec_()