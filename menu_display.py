__author__ = 'c0stos3'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os
import ConfigParser
import base64
import zlib
from Conf import Server

class settings_display(QMainWindow):
    def __init__(self, parent=None, Server=None):
        super(settings_display, self).__init__(None)
        #add all keywords to object
        self.server = Server
        self.setFixedSize(200, 300)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Zenstamon Settings')
        self.configfile = os.path.expanduser('~') + os.sep + "zenstamon.conf"
        self.createMenu()
        self.readConfigData()


    def readConfigData(self):
        if os.path.exists(self.configfile):
            print self.server.server_url
            self.serverTxt.setText(self.server.server_url)
            self.serverTxt.repaint()
            self.PortTxt.setText(self.server.server_port)
            self.PortTxt.repaint()
            self.usernameTxt.setText(self.server.username)
            self.usernameTxt.repaint()
            self.passwordTxt.setText(self.server.password)

            self.passwordTxt.repaint()

    def createMenu(self):
        self.tabbar = QTabWidget(self)

        self.createHomepage()
        self.serverInfoTab()

        self.tabbar.addTab(self.hometab, "Home")
        self.tabbar.addTab(self.servertab, "server")
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
        hostLbl = QLabel("Server: ")
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

    def createButtons(self):
        b = 3

    def quit(self):
        self.hide()

    def savePage(self):
        #check if file exists, if so read from file
        if  os.path.exists(self.configfile):
            config = ConfigParser.ConfigParser()
            config.add_section("Zenstamon")
            config.set("Zenstamon", "Server", self.serverTxt.text())
            config.set("Zenstamon", "Port", self.PortTxt.text())
            tmpUsr = self.usernameTxt.text()
            tmpUsr = self.Obfuscate(tmpUsr)
            config.set("Zenstamon", "User", tmpUsr)
            encryptPass = self.passwordTxt.text()
            encryptPass = self.Obfuscate(encryptPass)
            config.set("Zenstamon", "Password", encryptPass)
            os.remove(self.configfile)
            f = open(os.path.normpath(self.configfile), "w")
            config.write(f)
            f.close()

            #file does not exist and we create one.
        else:
            config = ConfigParser.ConfigParser()
            config.add_section("Zenstamon")
            config.set("Zenstamon", "Server", self.serverTxt.text())
            config.set("Zenstamon", "Port", self.PortTxt.text())
            tmpUsr = self.usernameTxt.text()
            tmpUsr = self.Obfuscate(tmpUsr)
            config.set("Zenstamon", "User", tmpUsr)
            encryptPass = self.passwordTxt.text()
            encryptPass = self.Obfuscate(encryptPass)
            config.set("Zenstamon", "Password", encryptPass)

            f = open(os.path.normpath(self.configfile), "w")
            config.write(f)
            f.close()

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