__author__ = 'c0stos3'

from zenoss_api import *
import json
import urllib
import urllib2

z = ZenossAPIExample()
#events = z.get_event()

isset = z.set_event_ack('00217038-2d84-a039-11e2-2815a9744636')
isset = z.remove_event_ack('00217038-2d84-a039-11e2-2815a9744636')
isset = z.remove_event('00217038-2d84-a039-11e2-2815a9744636')
print json.dumps(isset)