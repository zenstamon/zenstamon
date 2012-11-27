# Zenoss-4.x JSON API Example (python)
#
# To quickly explore, execute 'python -i zenoss_api.py'
#
# >>> z = ZenossAPIExample()
# >>> events = z.get_events()
# etc.

import json
import urllib
import urllib2
import ConfigParser
import os
from Conf import *
import base64
import zlib


ZENOSS_INSTANCE = ''
ZENOSS_USERNAME = ''
ZENOSS_PASSWORD = ''

ROUTERS = {'MessagingRouter': 'messaging',
           'EventsRouter': 'evconsole',
           'ProcessRouter': 'process',
           'ServiceRouter': 'service',
           'DeviceRouter': 'device',
           'NetworkRouter': 'network',
           'TemplateRouter': 'template',
           'DetailNavRouter': 'detailnav',
           'ReportRouter': 'report',
           'MibRouter': 'mib',
           'ZenPackRouter': 'zenpack'}

class ZenossAPIExample():
    def __init__(self, debug=False, Server=None):
        """
        Initialize the API connection, log in, and store authentication cookie
        """

        self.set_config_data(Server)
        # Use the HTTPCookieProcessor as urllib2 does not save cookies by default
        self.urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        if debug: self.urlOpener.add_handler(urllib2.HTTPHandler(debuglevel=1))
        self.reqCount = 1

        # Contruct POST params and submit login.
        loginParams = urllib.urlencode(dict(
            __ac_name=self.ZENOSS_USERNAME,
            __ac_password=self.ZENOSS_PASSWORD,
            submitted='true',
            came_from=self.ZENOSS_INSTANCE + '/zport/dmd'))
        self.urlOpener.open(self.ZENOSS_INSTANCE + '/zport/acl_users/cookieAuthHelper/login',
            loginParams)

    def set_config_data(self, Server):
        if True:
            self.ZENOSS_INSTANCE = 'http://' + Server.server_url + ':' + Server.server_port
            #print self.ZENOSS_INSTANCE
            self.ZENOSS_USERNAME = Server.username
            self.ZENOSS_PASSWORD = Server.password
            #print(ZENOSS_INSTANCE)
        else:
        #print("no config file found")
            pass


    def _router_request(self, router, method, data=[]):
        if router not in ROUTERS:
            raise Exception('Router "' + router + '" not available.')

        # Contruct a standard URL request for API calls
        req = urllib2.Request(self.ZENOSS_INSTANCE + '/zport/dmd/' +
                              ROUTERS[router] + '_router')

        # NOTE: Content-type MUST be set to 'application/json' for these requests
        req.add_header('Content-type', 'application/json; charset=utf-8')

        # Convert the request parameters into JSON
        reqData = json.dumps([dict(
            tid=self.reqCount,
            type='rpc',
            data=data,
            method=method,
            action=router)])

        #print(reqData)
        # Increment the request count ('tid'). More important if sending multiple
        # calls in a single request
        self.reqCount += 1

        # Submit the request and convert the returned JSON to objects
        return json.loads(self.urlOpener.open(req, reqData).read())

    #Working API
    def get_event(self, device=None, component=None, eventClass=None):
        data = dict(start=0, limit=500, dir='ASC', sort='severity')
        data['uid'] = '/zport/dmd'
        data['sort'] = 'device'
        data['keys'] = ['eventState', 'severity', 'device', 'component', 'eventClass', 'message', 'firstTime',
                        'lastTime', 'count', 'DevicePriority', 'evid', 'eventClassKey']
        data['params'] = dict(severity=[5, 4, 3], eventState=[0, 1], tags=[])

        if device: data['params']['device'] = device
        if component: data['params']['component'] = component
        if eventClass: data['params']['eventClass'] = eventClass

        return self._router_request('EventsRouter', 'query', [data])['result']

    def set_event_ack(self, evids):
        data = dict(limit=100)
        data['evids'] = [evids]
        return self._router_request('EventsRouter', 'acknowledge', [data])['result']

    def remove_event_ack(self, evids):
        data = dict(limit=100)
        data['evids'] = [evids]
        return self._router_request('EventsRouter', 'reopen', [data])['result']

    def remove_event(self, evids):
        data = dict(limit=100)
        data['evids'] = [evids]
        return self._router_request('EventsRouter', 'close', [data])['result']


    #Not working API
    def get_events(self, device=None, component=None, eventClass=None):
        data = dict(start=0, limit=200, dir='DESC', sort='severity')
        data['params'] = dict(severity=[5, 4, 3], eventState=[0, 1])

        if device: data['params']['device'] = device
        if component: data['params']['component'] = component
        if eventClass: data['params']['eventClass'] = eventClass

        return self._router_request('EventsRouter', 'query', [data])['result']

    def get_devices(self, deviceClass='/zport/dmd/Devices'):
        return self._router_request('DeviceRouter', 'getDevices',
            data=[{'uid': deviceClass,
                   'params': {}}])['result']


    def get_device_incomplete(self, device=None, component=None, eventClass=None):
        data = dict(start=0, limit=100, dir='DESC', sort='severity')
        data['uid'] = '/zport/dmd/Devices'
        data['sort'] = 'name'
        data['keys'] = ['name', 'ipAddress', 'uid', 'productionState', 'events', 'ipAddressString', 'pythonClass']
        #data['params'] = dict(severity=[5,4,3,2], eventState=[0,1],tags=[])

        if device: data['params']['device'] = device
        if component: data['params']['component'] = component
        if eventClass: data['params']['eventClass'] = eventClass

        return self._router_request('DeviceRouter', 'getDevices', [data])['result']

    def get_device(self, device=None, component=None, eventClass=None):
        data = dict(start=0, limit=100, dir='DESC', sort='severity')
        data['uid'] = '/zport/dmd/Devices'
        data['sort'] = 'name'
        data['keys'] = ['name', 'ipAddress', 'uid', 'productionState', 'events', 'ipAddressString', 'pythonClass']
        data['params'] = dict(severity=[5, 4, 3, 2], eventState=[0, 1], tags=[])

        if device: data['params']['device'] = device
        if component: data['params']['component'] = component
        if eventClass: data['params']['eventClass'] = eventClass

        return self._router_request('DeviceRouter', 'getInfo', [data])['result']

    def add_device(self, deviceName, deviceClass):
        data = dict(deviceName=deviceName, deviceClass=deviceClass)
        return self._router_request('DeviceRouter', 'addDevice', [data])

    def create_event_on_device(self, device, severity, summary):
        if severity not in ('Critical', 'Error', 'Warning', 'Info', 'Debug', 'Clear'):
            raise Exception('Severity "' + severity + '" is not valid.')

        data = dict(device=device, summary=summary, severity=severity,
            component='', evclasskey='', evclass='')
        return self._router_request('EventsRouter', 'add_event', [data])


        

