__author__ = 'c0stos3'
from PyQt4 import QtCore
from PyQt4.QtCore import (QThread, pyqtSignal)
import time



class refresh_Thread(QtCore.QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.stars = 0


    refresh = pyqtSignal()

    def run(self):
        #give enough time for the app to load and initialize
        time.sleep(60)
        while True:
            time.sleep(60)

            self.emit(QtCore.SIGNAL("refreshData()"))
            #print("refresh emit")

