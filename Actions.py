__author__ = 'milleju'
import subprocess
import threading
import time
from PyQt4 import QtCore
from PyQt4.QtCore import (QThread, pyqtSignal)

import platform

if platform.system() == "Windows":
    import winsound

class RefreshLoop(QtCore.QThread):
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

REGISTERED_SERVERS = []

def register_server(server):
    """ Once new server class in created,
    should be registered with this function
    for being visible in config and
    accessible in application.
    """
    REGISTERED_SERVERS.append((server.TYPE, server))


def get_registered_servers():
    """ Returns available server classes dict """
    return dict(REGISTERED_SERVERS)


def CreateServer(server=None, conf=None, resources=None):
# create Server from config
# give argument servername so CentreonServer could use it for initializing MD5 cache
    registered_servers = get_registered_servers()
    zenossserver = registered_servers[server.type](conf=conf, name=server.name)
    zenossserver.server_url = server.server_url
    zenossserver.server_port = server.server_port
    # add resources, needed for auth dialog
    #zenossserver.Resources = resources
    zenossserver.username = server.username
    zenossserver.password = server.password

    return zenossserver


class PlaySound(threading.Thread):
    """
        play notification sound in a threadified way to omit hanging gui
    """

    def __init__(self, **kwds):
        # add all keywords to object, every mode searchs inside for its favorite arguments/keywords
        for k in kwds: self.__dict__[k] = kwds[k]
        threading.Thread.__init__(self)
        self.setDaemon(1)


    def run(self):
        if self.sound == "WARNING":
            if str(self.conf.notification_default_sound) == "True":
                self.Play(self.Resources + "/warning.wav")
            else:
                self.Play(self.conf.notification_custom_sound_warning)
        elif self.sound == "CRITICAL":
            if str(self.conf.notification_default_sound) == "True":
                self.Play(self.Resources + "/critical.wav")
            else:
                self.Play(self.conf.notification_custom_sound_critical)
        elif self.sound == "DOWN":
            if str(self.conf.notification_default_sound) == "True":
                self.Play(self.Resources + "/hostdown.wav")
            else:
                self.Play(self.conf.notification_custom_sound_down)
        elif self.sound == "FILE":
            self.Play(self.file)


    def Play(self, file):
        """
            depending on platform choose method to play sound
        """
        # debug
        if str(self.conf.debug_mode) == "True":
            # once again taking .Debug() from first server
            self.servers.values()[0].Debug(debug="Playing sound: " + str(file))
        if not platform.system() == "Windows":
            subprocess.Popen("play -q %s" % str(file), shell=True)
        else:
            winsound.PlaySound(file, winsound.SND_FILENAME)