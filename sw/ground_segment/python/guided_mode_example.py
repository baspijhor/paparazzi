#!/usr/bin/env python

from __future__ import print_function

import sys
from os import path, getenv

# if PAPARAZZI_SRC not set, then assume the tree containing this
# file is a reasonable substitute
PPRZ_SRC = getenv("PAPARAZZI_SRC", path.normpath(path.join(path.dirname(path.abspath(__file__)), '../../../../')))
sys.path.append(PPRZ_SRC + "/sw/lib/python")

from ivy_msg_interface import IvyMessagesInterface
from pprz_msg.message import PprzMessage
from settings_xml_parse import PaparazziACSettings

from math import radians
from time import sleep

class Guidance(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self._interface = IvyMessagesInterface(self.message_recv)

    def message_recv(self, ac_id, msg):
        if self.verbose:
            print("Got msg %s" % msg.name)

    def shutdown(self):
        print("Shutting down ivy interface...")
        self._interface.shutdown()

    def __del__(self):
        self.shutdown()

    def set_guided_mode(self, ac_id):
        """
        change auto2 mode to GUIDED.
        """
        settings = PaparazziACSettings(ac_id)
        try:
            index = settings.name_lookup['auto2'].index
        except Exception as e:
            print(e)
            index = 1
        msg = PprzMessage("ground", "DL_SETTING")
        msg['ac_id'] = ac_id
        msg['index'] = index
        msg['value'] = 19 # AP_MODE_GUIDED
        print("Sending message: %s" % msg)
        self._interface.send(msg)

    def goto(self, ac_id, north, east, down, heading):
        """
        goto a local NorthEastDown position in meters (if already in GUIDED mode)
        """
        msg = PprzMessage("ground", "DL_POSITION_TARGET_LOCAL_NED")
        msg['ac_id'] = ac_id
        msg['x'] = north
        msg['y'] = east
        msg['z'] = down
        msg['heading'] = heading
        print("Sending message: %s" % msg)
        self._interface.send(msg)


if __name__ == '__main__':
    ac_id = 42
    g = Guidance()
    sleep(0.1)
    g.set_guided_mode(ac_id)
    sleep(0.1)
    g.goto(ac_id=ac_id, north=5.0, east=10.0, down=-5.0, heading=radians(90))
    sleep(0.5)
    g.shutdown()
