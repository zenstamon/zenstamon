__author__ = 'c0stos3'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os
import ConfigParser
import base64
import zlib
from Conf import Server
import ast


class settings_display(QMainWindow):
    def __init__(self, parent=None):
        super(settings_display, self).__init__(None)
        #add all keywords to object
        self.server = None
        self.setFixedSize(250, 300)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Zenstamon Settings')
        self.configfile = os.path.expanduser('~') + os.sep + "zenstamon.conf"
        self.createMenu()


    def setConfigData(self, conf):
        #print self.server.server_url
        self.serverTxt.setText(conf.server.server_url)
        self.serverTxt.repaint()
        self.PortTxt.setText(conf.server.server_port)
        self.PortTxt.repaint()
        self.usernameTxt.setText(conf.server.username)
        self.usernameTxt.repaint()
        self.passwordTxt.setText(conf.server.password)
        self.passwordTxt.repaint()

        #events tab

        self.hostcol.setChecked(ast.literal_eval(conf.eventConf.host))
        self.statecol.setChecked(ast.literal_eval(conf.eventConf.state))
        self.messagecol.setChecked(ast.literal_eval(conf.eventConf.message))
        self.firstTimeCol.setChecked(ast.literal_eval(conf.eventConf.first))
        self.lastTimeCol.setChecked(ast.literal_eval(conf.eventConf.last))
        self.countcol.setChecked(ast.literal_eval(conf.eventConf.count))
        self.eventclasscol.setChecked(ast.literal_eval(conf.eventConf.eventclass))
        self.refreshTxt.setText(conf.eventConf.duration)


    def createMenu(self):
        self.tabbar = QTabWidget(self)

        self.createHomepage()
        self.serverInfoTab()
        self.eventConfig()
        self.tabbar.addTab(self.hometab, "Home")
        self.tabbar.addTab(self.servertab, "Server")
        self.tabbar.addTab(self.eventtab, "Event")
        self.setCentralWidget(self.tabbar)


    def createHomepage(self):
        self.hometab = QWidget()
        btnLayout = QHBoxLayout()
        self.saveHBtn = QPushButton("Save")
        self.cancelHBtn = QPushButton("Cancel")
        welcomeLbl = QLabel("Welcome to Zenstamon Config")
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(welcomeLbl)
        mainLayout.insertStretch(5)

        btnLayout.addWidget(self.saveHBtn)
        btnLayout.addWidget(self.cancelHBtn)
        mainLayout.addItem(btnLayout)
        self.hometab.setLayout(mainLayout)

    def serverInfoTab(self):
        self.servertab = QWidget()
        btnLayout = QHBoxLayout()
        self.saveSBtn = QPushButton("Save")
        self.cancelSBtn = QPushButton("Cancel")
        mainLayout = QVBoxLayout()

        #Server info
        hostLayout = QHBoxLayout()
        hostLbl = QLabel("IP Address: ")
        self.serverTxt = QLineEdit()
        self.serverTxt.setInputMethodHints(Qt.ImhUrlCharactersOnly)
        hostLayout.addWidget(hostLbl)
        hostLayout.insertStretch(1)
        hostLayout.addWidget(self.serverTxt)
        mainLayout.addItem(hostLayout)

        #Port Info
        PortLayout = QHBoxLayout()
        PortLbl = QLabel("Port: ")
        self.PortTxt = QLineEdit()
        self.PortTxt.setInputMethodHints(Qt.ImhDigitsOnly)

        PortLayout.addWidget(PortLbl)
        PortLayout.insertStretch(1)
        PortLayout.addWidget(self.PortTxt)
        mainLayout.addItem(PortLayout)
        #Username Info
        usernameLayout = QHBoxLayout()
        usernameLbl = QLabel("Username: ")
        self.usernameTxt = QLineEdit()

        usernameLayout.addWidget(usernameLbl)
        usernameLayout.insertStretch(1)
        usernameLayout.addWidget(self.usernameTxt)
        mainLayout.addItem(usernameLayout)
        #Password info
        passwordLayout = QHBoxLayout()
        passwordLbl = QLabel("Password: ")
        self.passwordTxt = QLineEdit()
        self.passwordTxt.setEchoMode(QLineEdit.Password)
        passwordLayout.addWidget(passwordLbl)
        passwordLayout.insertStretch(1)
        passwordLayout.addWidget(self.passwordTxt)
        mainLayout.addItem(passwordLayout)

        mainLayout.insertStretch(5)
        #Buttons
        btnLayout.addWidget(self.saveHBtn)
        btnLayout.addWidget(self.cancelHBtn)
        mainLayout.addItem(btnLayout)

        self.connect(self.saveHBtn, SIGNAL("clicked()"), self.savePage)
        self.connect(self.cancelHBtn, SIGNAL("clicked()"), self.quit)
        self.servertab.setLayout(mainLayout)

    def eventConfig(self):
        self.eventtab = QWidget()
        btnLayout = QHBoxLayout()
        self.saveEBtn = QPushButton("Save")
        self.cancelEBtn = QPushButton("Cancel")
        mainLayout = QVBoxLayout()

        #Refresh Duration
        refreshLayout = QHBoxLayout()
        hostLbl = QLabel("Refresh Interval: ")
        topLbl = QLabel("Select Columns to view")

        self.refreshTxt = QLineEdit()
        self.refreshTxt.setInputMethodHints(Qt.ImhDigitsOnly)
        self.refreshTxt.setMaximumWidth(40)

        refreshLayout.addWidget(hostLbl)
        refreshLayout.insertStretch(1)
        refreshLayout.addWidget(self.refreshTxt)
        mainLayout.addItem(refreshLayout)

        mainLayout.addWidget(topLbl)

        #Event column options
        self.firstTimeCol = QCheckBox("First Seen")
        self.lastTimeCol = QCheckBox("Last Seen")
        self.countcol = QCheckBox("Count")
        self.messagecol = QCheckBox("Message")
        self.hostcol = QCheckBox("Host")
        self.statecol = QCheckBox("Status")
        self.eventclasscol = QCheckBox("Event Class")
        mainLayout.addWidget(self.hostcol)
        mainLayout.addWidget(self.statecol)
        mainLayout.addWidget(self.messagecol)
        mainLayout.addWidget(self.firstTimeCol)
        mainLayout.addWidget(self.lastTimeCol)
        mainLayout.addWidget(self.countcol)
        mainLayout.addWidget(self.eventclasscol)
        self.hostcol.setChecked(True)
        self.statecol.setChecked(True)
        self.messagecol.setChecked(True)

        mainLayout.stretch(0)
        #Buttons
        btnLayout.addWidget(self.saveEBtn)
        btnLayout.addWidget(self.cancelEBtn)
        mainLayout.addItem(btnLayout)

        self.connect(self.saveEBtn, SIGNAL("clicked()"), self.savePage)
        self.connect(self.cancelEBtn, SIGNAL("clicked()"), self.quit)
        self.eventtab.setLayout(mainLayout)

    def quit(self):
        self.hide()

    menuSaveClick = pyqtSignal()

    def savePage(self):
        config = ConfigParser.ConfigParser()
        config.add_section("Server")
        config.set("Server", "server_url", self.serverTxt.text())
        config.set("Server", "server_port", self.PortTxt.text())
        tmpUsr = self.usernameTxt.text()
        tmpUsr = self.Obfuscate(tmpUsr)
        config.set("Server", "username", tmpUsr)
        encryptPass = self.passwordTxt.text()
        encryptPass = self.Obfuscate(encryptPass)
        config.set("Server", "password", encryptPass)

        config.add_section("Events")
        config.set("Events", "duration", self.refreshTxt.text())
        config.set("Events", "host", self.hostcol.isChecked())
        config.set("Events", "state", self.statecol.isChecked())
        config.set("Events", "message", self.messagecol.isChecked())
        config.set("Events", "first_seen", self.firstTimeCol.isChecked())
        config.set("Events", "last_seen", self.lastTimeCol.isChecked())
        config.set("Events", "count", self.countcol.isChecked())
        config.set("Events", "event_class", self.eventclasscol.isChecked())

        #check if file exists, if so read from file
        if  os.path.exists(self.configfile):
            os.remove(self.configfile)
        f = open(os.path.normpath(self.configfile), "w")
        config.write(f)
        f.close()

        self.hide()
        self.menuSaveClick.emit()


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.pos()
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos().x() - self.drag_position.x(), event.globalPos().y() - self.drag_position.y())
            event.accept()

    def Obfuscate(self, string, count=5):
        """
            Obfuscate a given string to store passwords etc.
        """
        string2 = string
        for i in range(count):
            string = list(base64.b64encode(string))
            string.reverse()
            string = "".join(string)
            string = zlib.compress(string)
        string = base64.b64encode(string)
        return string2


    def DeObfuscate(self, string, count=5):
        string2 = string
        '''string = base64.b64decode(string)
        for i in range(count):
            string = zlib.decompress(string)
            string = list(string)
            string.reverse()
            string = "".join(string)
            string = base64.b64decode(string)
        '''
        return str(string2)