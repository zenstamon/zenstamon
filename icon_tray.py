import sys
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os

class SystemTrayIcon(QtGui.QSystemTrayIcon):
    displaySummWindow = pyqtSignal()

    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.setParent(parent)

        if getattr(sys, 'frozen', None):
            self.basedir = sys._MEIPASS + "\\resources\\"
            print("exe-directory-files")
        else:
            self.basedir = os.path.dirname("resources/")

        self.menu = QtGui.QMenu(parent)
        self.action_show = QtGui.QAction(u'Display App', self)
        self.action_show_summary = QtGui.QAction(u'Display Summary', self)
        self.action_warn = QtGui.QAction(u'Warn', self)
        self.action_quit = QtGui.QAction(u'Quit', self)
        self.action_crit = QtGui.QAction(u'Critical', self)
        self.action_ok = QtGui.QAction(u'OK', self)

        self.connect(self.action_quit, SIGNAL("triggered()"), QtGui.qApp.quit)
        self.connect(self.action_warn, SIGNAL("triggered()"), self.set_icon_warn)
        self.connect(self.action_crit, SIGNAL("triggered()"), self.set_icon_critical)
        self.connect(self.action_ok, SIGNAL("triggered()"), self.set_icon_ok)
        self.connect(self.action_show, SIGNAL("triggered()"), self.display_app)
        self.connect(self.action_show_summary, SIGNAL("triggered()"), self.display_summ)
        self.connect(self, SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.cb_systray_activated)
        #traySignal = "activated(QSystemTrayIcon::ActivationReason)"
        #self.connect(self, SIGNAL("triggered()"), self.icon_activated)
        #self.activated.connect(self.icon_activated)

        self.menu.addAction(self.action_show)
        self.menu.addAction(self.action_show_summary)
        separator = QtGui.QAction(self)
        separator.setSeparator(True)
        self.menu.addAction(separator)
        self.menu.addAction(self.action_ok)
        self.menu.addAction(self.action_warn)
        self.menu.addAction(self.action_crit)
        separator2 = QtGui.QAction(self)
        separator2.setSeparator(True)
        self.menu.addAction(separator2)
        self.menu.addAction(self.action_quit)
        self.setContextMenu(self.menu)
        self.ActivationReason

        #TODO -- add error as option


    def cb_systray_activated(self, reason):
        #print(reason)
        #self.showMessage("test","test2")
        pass

    def set_icon_warn(self, play):
        warnIcon = QtGui.QIcon(self.basedir + "/Zenoss_O_yellow.png")
        path = os.path.join(self.basedir, "warning.wav")
        if play == True:
            QtGui.QSound(path).play()
            #print("play warning")
        self.setIcon(warnIcon)

    def set_icon_critical(self, play):
        relativename = "Zenoss_O_red.png"
        path = os.path.join(self.basedir, relativename)
        warnIcon = QtGui.QIcon(path)
        path = os.path.join(self.basedir, "critical.wav")
        if play == True:
            QtGui.QSound(path).play()
            #print("Play critical")
        self.setIcon(warnIcon)
        #print(path)

    def set_icon_ok(self):
        warnIcon = QtGui.QIcon(self.basedir + "/Zenoss_O_green.png")
        self.setIcon(warnIcon)

    def display_app(self):
        self.parent().show()

        #parent.show()


    def display_summ(self):
        self.displaySummWindow.emit()

    def icon_activated(self, reason):
        #print("click happened!!!!")
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.show()
            #print("double click happened!!!!")

