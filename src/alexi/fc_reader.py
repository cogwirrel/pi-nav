import os
import arrow
from threading import Thread
import alexi.server as server
from alexi.fc_utils import FcLogger
import time

class FcReader(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.active = True
        self.fc_logger = FcLogger('/dev/ttyECU')
 
    def run(self):
        while self.active:
            # Read some data from the powerfc
            data = self.fc_logger.read_one()

            # data = {
            #     'Engine Speed(rpm)': str(1000 + i),
            #     'Absolute Intake Pressure(Kg/cm^2)': '',
            #     'Pressure Sensor Voltage(mV)': '',
            #     'Throttle Voltage(mV)': '',
            #     'Primary Injector Pulse Width(mSec)': '',
            #     'Fuel Correction': '',
            #     'Leading Ignition Angle(deg)': '',
            #     'Trailing Ignition Angle(deg)': '',
            #     'Fuel Temperature(deg.C)': '',
            #     'Metalling Oil PumpDuty(%)': '',
            #     'Boost Duty(Tp, %)': '',
            #     'Boost Duty(Wg, %)': '',
            #     'Water Temperature(deg.C)': '',
            #     'Intake Air Temperature(deg.C)': '',
            #     'Knocking Level': '',
            #     'Battery Voltage(V)': '',
            #     'Vehicle Speed(Km/h)': '',
            #     'ISCV duty(%)': '',
            #     'O2 Sensor Voltage(mV)': '',
            #     'N/A': '',
            #     'Secondary Injector Pulse Width(mSec)': '',
            #     'N/A': '',
            # }
            #print data

            server.send_ecu_update(data)
            time.sleep(0.2)

    def stop(self):
        self.active = False
        self.fc_logger.close()
 

_fc_reader = None


def start():
    global _fc_reader
    if _fc_reader is not None:
        _fc_reader.stop()
    
    _fc_reader = FcReader()
    _fc_reader.start()


def stop():
    global _fc_reader
    _fc_reader.stop()
    _fc_reader = None
