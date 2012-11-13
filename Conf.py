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
                    print i[0] + " " + i[1]
                    self.unconfigured = False
            print self.__dict__;

            self.server.server_url = self.__dict__['server_url']
            self.server.server_port = self.__dict__['server_port']
            self.server.username = self.__dict__['username']
            self.server.password = self.__dict__['password']

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
