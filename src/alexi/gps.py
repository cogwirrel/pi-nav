import os
from gps import gps
import arrow
from threading import Thread
 
class GpsListener(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.gps_listener = gps(mode=WATCH_ENABLE)
        self.active = True
 
    def run(self):
        while self.active:
            # Get updates gps_listener with the latest data
            self.gps_listener.next()

    def get(self):
        return self.gps_listener

    def stop(self):
        self.active = False
 

_gps_listener = None

def start():
    if _gps_listener is not None:
        _gps_listener.stop()
        _gps_listener.join()
    
    _gps_listener = GpsListener()
    _gps_listener.start()

def get_data():
    gps_info = _gps_listener.get()

    return {
        'latitude': gps_info.fix.latitude,
        'longitude': gps_info.fix.longitude,
        'altitude': gps_info.fix.altitude,
        'speed': gps_info.fix.speed,
        'climb': gps_info.fix.climb,
        'track': gps_info.fix.track,
        'satellites': gps_info.satellites,
        'timestamp': arrow.get(gps_info.utc + 'T' + gps_info.fix.time)
    }

def stop():
    _gps_listener.stop()
    _gps_listener.join()
    _gps_listener = None