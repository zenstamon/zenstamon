__author__ = 'c0stos3'
from PyQt4 import QtCore
from PyQt4.QtCore import (QThread, pyqtSignal)
import time
from zenoss_actions import *
from events import *


class refresh_Thread(QtCore.QThread):
    def __init__(self, parent=None, server=None, refreshTime=60):
        QThread.__init__(self, parent)
        self.exiting = False
        self.stars = 0
        self.server = server
        self.refreshTime = refreshTime

    def run(self):
        #give enough time for the app to load and initialize
        #time.sleep(60)
        while True:
            #print(self.refreshTime)
            time.sleep(int(self.refreshTime))

            self.zen_get = zenoss_actions(Server=self.server)

            self.events = self.zen_get.getEvents()

            self.emit(QtCore.SIGNAL("refreshData(PyQt_PyObject)"), self.events)
            #print("refresh emit")






