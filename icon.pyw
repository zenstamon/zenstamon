import sys
import time
from zenoss_api import *
import winsound
from PyQt4 import QtGui
from PyQt4.QtCore import (Qt, SIGNAL, SLOT)
from PyQt4.QtGui import QDialog, QApplication, QTableWidget, QTableWidgetItem
from PyQt4.uic import *
from alertview import Ui_Dialog


class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)

        self.menu = QtGui.QMenu(parent)
        self.action_warn = QtGui.QAction(u'Warn', self)
        self.action_quit = QtGui.QAction(u'Quit', self)
        self.action_crit = QtGui.QAction(u'Critical', self)
        self.action_ok = QtGui.QAction(u'OK', self)

        self.connect(self.action_quit, SIGNAL("triggered()"), QtGui.qApp.quit)
        self.connect(self.action_warn, SIGNAL("triggered()"), self.set_icon_warn)
        self.connect(self.action_crit, SIGNAL("triggered()"), self.set_icon_critical)
        self.connect(self.action_ok, SIGNAL("triggered()"), self.set_icon_ok)

        self.menu.addAction(self.action_ok)
        self.menu.addAction(self.action_warn)
        self.menu.addAction(self.action_crit)
        self.menu.addAction(self.action_quit)
        self.setContextMenu(self.menu)

    def set_icon_warn(self):
        warnIcon = QtGui.QIcon("resources/Zenoss_O_yellow.png")
        winsound.PlaySound("resources/warning.wav", winsound.SND_FILENAME)
        self.setIcon(warnIcon)

    def set_icon_critical(self):
        warnIcon = QtGui.QIcon("resources/Zenoss_O_red.png")
        winsound.PlaySound("resources/critical.wav", winsound.SND_FILENAME)
        self.setIcon(warnIcon)

    def set_icon_ok(self):
        warnIcon = QtGui.QIcon("resources/Zenoss_O_green.png")
        self.setIcon(warnIcon)


class MyTable(QTableWidget):
    def __init__(self, thestruct, *args):
        QTableWidget.__init__(self, *args)
        self.data = thestruct
        self.setmydata()

    def setmydata(self):
        n = 0
        for key in self.data:
            m = 0
            for item in self.data[key]:
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
                m += 1
            n += 1


def main():
    app = QtGui.QApplication(sys.argv)
    window = QDialog()
    ui = Ui_Dialog()

    #while(True):
    z = ZenossAPIExample()
    events = z.get_event()
    critical = 0
    error = 0
    warning = 0
    total = 0

    server = []
    status = []
    message = []
    mystruct = {'SERVER': server, 'STATUS': status, 'MESSAGE': message}

    ui.setupUi(window)
    ui.tableWidget.setRowCount(10)
    for e in events['events'][:]:
        if e['severity'] == 5:
            #message.append(e['device']['text'])
            #status.append('CRITICAL')
            #server.append(e['component']['text'])
            critical = critical + 1
            total = total + 1
            ui.tableWidget.setItem(total, 0, QTableWidgetItem(str(e['device']['text'])))
            ui.tableWidget.setItem(total, 1, QTableWidgetItem('CRITICAL'))
            ui.tableWidget.setItem(total, 2, QTableWidgetItem(str(e['message'])))
        elif e['severity'] == 4:
            #message.append(e['device']['text'])
            #status.append('ERROR')
            #server.append(e['component']['text'])
            error = error + 1
            total = total + 1
            ui.tableWidget.setItem(total, 0, QTableWidgetItem(str(e['device']['text'])))
            ui.tableWidget.setItem(total, 1, QTableWidgetItem('ERROR'))
            ui.tableWidget.setItem(total, 2, QTableWidgetItem(str(e['message'])))
        elif e['severity'] == 3:
            #message.append(e['device']['text'])
            #status.append('WARNING')
            #server.append(e['component']['text'])
            warning = warning + 1
            total = total + 1
            ui.tableWidget.setItem(total, 0, QTableWidgetItem(str(e['device']['text'])))
            ui.tableWidget.setItem(total, 1, QTableWidgetItem('ERROR'))
            ui.tableWidget.setItem(total, 2, QTableWidgetItem(str(e['message'])))


            #message.append(json.dumps(e['device']['text']))
            #status.append(json.dumps(e['severity']))
            #server.append(json.dumps(e['component']['text']))
            #   time.sleep(10)

    #ui.setupUi(window)

    #ui.tableWidget.setRowCount(server.count())
    #n = 0
    #for key in mystruct:
    #    m = 0
    #    for item in mystruct[key]:
    #        print item
    #        newitem = QTableWidgetItem(item)
    #        ui.tableWidget.setItem(m, n, newitem)
    #        m += 1
    #    n += 1
    #QTableWidgetItem *newItem = new QTableWidgetItem(tr("%1").arg(pow(row, column+1)));
    #item = QtGui.QTableWidgetItem("data1")
    #ui.tableWidget.setItem(1,1,item)
    window.show()
    w = QtGui.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("resources/Zenoss_O_green.png"), w)
    if (critical > 0):
        trayIcon.action_crit.trigger()
    elif (warning > 0 or error > 0):
        trayIcon.action_warn.trigger()
    else:
        trayIcon.action_ok.trigger()
    trayIcon.show()

    sys.exit(app.exec_())

#def on_Button_clicked(self, checked=None):
#    if checked==None: return
#    dialog = QDialog()
#    dialog.ui = Ui_MyDialog()
#    dialog.ui.setupUi(dialog)
#    dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
#    dialog.exec_()

if __name__ == '__main__':
    main()