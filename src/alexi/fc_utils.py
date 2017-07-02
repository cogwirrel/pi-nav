#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time
import sys
import os
import logging
from datetime import datetime
from struct import unpack_from

class FcLogger:
    """ FC Logger class - thanks to the guys at Raspexi/Powertune for this!
    """
    FC_ADV_INFO_LEN = 0x20
    FC_REQ_ADV_INFO = '\xF0\x02\x0D'
    FC_ADV_INFO_KEYS = ['Engine Speed(rpm)',
                        'Absolute Intake Pressure(Kg/cm^2)',
                        'Pressure Sensor Voltage(mV)',
                        'Throttle Voltage(mV)',
                        'Primary Injector Pulse Width(mSec)',
                        'Fuel Correction',
                        'Leading Ignition Angle(deg)',
                        'Trailing Ignition Angle(deg)',
                        'Fuel Temperature(deg.C)',
                        'Metalling Oil PumpDuty(%)',
                        'Boost Duty(Tp, %)',
                        'Boost Duty(Wg, %)',
                        'Water Temperature(deg.C)',
                        'Intake Air Temperature(deg.C)',
                        'Knocking Level',
                        'Battery Voltage(V)',
                        'Vehicle Speed(Km/h)',
                        'ISCV duty(%)',
                        'O2 Sensor Voltage(mV)',
                        'N/A',
                        'Secondary Injector Pulse Width(mSec)',
                        'N/A']
    FC_ADV_INFO_MUL = [1, 0.0001, 1, 1, 1.0/256, 1.0/256, 1, 1, 1, 212.0/256, 0.4, 0.4, 1, 1, 1, 0.1, 1, 0.1, 0.02, 1, 1.0/256, 1]
    FC_ADV_INFO_ADD = [0, 0, 0, 0, 0, 0, -25, -25, -80, 0, 0, 0, -80, -80, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, portName, baudRate=57600, timeout=1.0):
        self.portName = portName
        self.port = serial.Serial(self.portName,
                                  baudrate=baudRate,
                                  bytesize=serial.EIGHTBITS,
                                  stopbits=serial.STOPBITS_ONE,
                                  timeout=timeout,
                                  parity=serial.PARITY_NONE,
                                  rtscts=True)
        self.ilen = -1

    def close(self):
        self.port.close()

    def _write(self, buf):
        self.port.write(buf)

    def _read(self, length):
        buf = self.port.read(length)
        return buf

    def _getInfo(self, ilen=FC_ADV_INFO_LEN):
        self._write(self.FC_REQ_ADV_INFO)
        return self._read(ilen + 1)

    def _getInfoLength(self):
        buf = self._getInfo()
        if len(buf) >= (self.FC_ADV_INFO_LEN + 1):
            return ord(buf[1])
        else:
            return -1

    def _decode(self, buf):
        try:
            out = unpack_from('<HHHHHHBBBBBBBBBBHHBBHB', buf, offset=2)
            out = [a * b for a, b in zip(out, self.FC_ADV_INFO_MUL)]
            out = [a + b for a, b in zip(out, self.FC_ADV_INFO_ADD)]
            info = dict(zip(self.FC_ADV_INFO_KEYS, out))
        except Exception as ex:
            print(ex)
            return None
        return info

    def read_one(self):
        while self.ilen == -1:
            self.ilen = self._getInfoLength()
            time.sleep(1)

        buf = self._getInfo(self.ilen)
        info = self._decode(buf)

        return info

def str2hex(buf):
    """ Convert string buffer to hexadecimal
    """
    if len(buf):
        return " ".join([ "%02X" % ord(ch) for ch in buf ])
    else:
        return ""
