__author__ = 'c0stos3'

from zenoss_api import *

class zenoss_actions(object):
    def __init__(self, parent=None, Server=None):
        #perform zenoss actions against the events
        self.server = Server
        x = 0
        ########

    ##Get Zenoss Data
    ########

    def getEvents(self):
        z = ZenossAPIExample(Server=self.server)
        events = z.get_event()
        return events

    def summaryEvents(self, events ):
        critical = 0
        error = 0
        warning = 0
        info = 0
        debug = 0
        clear = 0
        for e in events['events'][:]:
            if e['severity'] == 5:
                critical = critical + 1
            elif e['severity'] == 4:
                error = error + 1
            elif e['severity'] == 3:
                warning = warning + 1
            elif e['severity'] == 2:
                info = info + 1
            elif e['severity'] == 1:
                debug = debug + 1
            elif e['severity'] == 0:
                clear = clear + 1
        totalRows = critical + error + warning + info
        severity = []
        severity.append(critical)
        severity.append(error)
        severity.append(warning)
        severity.append(info)
        severity.append(debug)
        severity.append(clear)

        return severity