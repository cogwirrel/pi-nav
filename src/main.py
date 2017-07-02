import logging

logging.basicConfig()

# Socketio doesn't work without this!
import eventlet
eventlet.monkey_patch()

import alexi.gps_reader as gps
import alexi.server as server
import alexi.iot.iot as iot
import alexi.db.db as db
import alexi.fc_reader as fc_reader
import time
import os

DB_UPLOAD_INTERVAL = 1.0

def init():
    # Init logic goes here
    fc_reader.start()
    gps.start()
    server.start()
    iot.start(on_shutdown=shutdown)

def shutdown(switch_off=False):
    iot.stop()
    server.stop()
    gps.stop()
    fc_reader.stop()
    if switch_off:
        os.system("sudo shutdown -h now")
    else:
        os._exit(0)

def main():
    init()

    try:
        # Handy for debugging!
        # import code
        # code.interact(local=locals())

        db.start_journey()

        while True:
            gps_data = gps.get_data()

            if str(gps_data['latitude']) != 'nan':
                db.set_current_gps_data(gps_data)
                #print gps_data

            time.sleep(DB_UPLOAD_INTERVAL)
    except (KeyboardInterrupt, SystemExit):
        print "Shutting down"
        shutdown()

if __name__ == '__main__':
    main()