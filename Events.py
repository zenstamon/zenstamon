__author__ = 'c0stos3'


########
##Event Data Class
########
class Event(object):
    def __init__(self, server=None, severity=None, message=None, eventid=None):
        self.server = server
        if severity == 5:
            self.severity = "CRITICAL"
        elif severity == 4:
            self.severity = "ERROR"
        elif severity == 3:
            self.severity = "WARNING"
        elif severity == 2:
            self.severity = "INFO"
        elif severity == 1:
            self.severity = "DEBUG"
        elif severity == 0:
            self.severity = "CLEAR"
        self.message = message
        self.eventid = eventid


