#!/usr/bin/env python
from ctypes import *
import sys
import random
import time

from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit

from pymongo import MongoClient

class SimplePhidget():

    def __init__(self):     
        try:
            self.interfaceKit = InterfaceKit()
        except RuntimeError as e:
            print("Runtime Exception: %s" % e.details)
            exit(1)

        print("Connecting to Phidget.")

        try:
            self.interfaceKit.openPhidget()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            exit(1)

        print("Connection opened.")

        try:
            self.interfaceKit.waitForAttach(10000)
        except PhidgetException as e:
            try:
                self.interfaceKit.closePhidget()
            except PhidgetException as e:
                exit(1)
            exit(1)
        print("Attached to phidget interface.")

    def getSensorValue(self, sensor):
        return self.interfaceKit.getSensorValue(sensor)

class SimpleMongo():

    def __init__(self, host, user, pswd, db):
        self.connection = MongoClient(host)
        self.db = self.connection[db]
        self.db.authenticate(user, pswd)

    def put(self, col, content):
        self.db[col].insert(content)


p = SimplePhidget()
m = SimpleMongo("host", "user", "pswd", "db")

m.put("light", {"date" : int(time.time()) , "value" : p.getSensorValue(3)})
m.put("humidity", {"date" : int(time.time()) , "value" : p.getSensorValue(0)})
m.put("temperature", {"date" : int(time.time()) , "value" : p.getSensorValue(1)})

