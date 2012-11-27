__author__ = 'milleju'
import os
import base64
import zlib
import ConfigParser

class Conf(object):
    def __init__(self):
        self.update_interval = 60
        self.unconfigured = True
        self.configfile = os.path.expanduser('~') + os.sep + "zenstamon.conf"
        self.server = Server()
        self.eventConf = EventColumns()
        self.server.server_url = ""
        self.server.server_port = ""
        self.server.username = ""
        self.server.password = ""
        if os.path.exists(self.configfile):
            config = ConfigParser.ConfigParser()
            config.read(self.configfile)

            for section in config.sections():
                for i in config.items(section):
                    object.__setattr__(self, i[0], i[1])
                    #print i[0] + " " + i[1]
                    self.unconfigured = False
                    #print(self.__dict__)

            self.server.server_url = self.__dict__['server_url']
            self.server.server_port = self.__dict__['server_port']
            self.server.username = self.__dict__['username']
            self.server.password = self.__dict__['password']

            self.eventConf.duration = self.__dict__['duration']
            self.eventConf.host = self.__dict__['host']
            self.eventConf.state = self.__dict__['state']
            self.eventConf.message = self.__dict__['message']
            self.eventConf.first = self.__dict__['first_seen']
            self.eventConf.last = self.__dict__['last_seen']
            self.eventConf.count = self.__dict__['count']
            self.eventConf.eventclass = self.__dict__['event_class']


    def createConfigFile(self):
        pass

    def Obfuscate(self, string, count=5):
        """
          Obfuscate a given string to store passwords etc.
        """
        for i in range(count):
            string = list(base64.b64encode(string))
            string.reverse()
            string = "".join(string)
            string = zlib.compress(string)
        string = base64.b64encode(string)
        return string


    def DeObfuscate(self, string, count=5):
        string = base64.b64decode(string)
        for i in range(count):
            string = zlib.decompress(string)
            string = list(string)
            string.reverse()
            string = "".join(string)
            string = base64.b64decode(string)
        return string


class Server(object):
    """
    one Server realized as object for config info
    """

    def __init__(self):
        self.server_url = ""
        self.server_port = ""
        self.username = ""
        self.password = ""


class EventColumns(object):
    """
    list of display options for events
    """

    def __init__(self):
        self.duration = "60"
        self.host = "True"
        self.state = "True"
        self.message = "True"
        self.first = "False"
        self.last = "False"
        self.count = "False"
        self.eventclass = "False"
