import alexi.gps_reader as gps
import alexi.server as server
import alexi.iot.iot as iot
import alexi.db.db as db
import time
import os

DB_UPLOAD_INTERVAL = 1.0

def init():
    # Init logic goes here
    gps.start()
    server.start()
    iot.start(on_shutdown=shutdown)

def shutdown(switch_off=False):
    iot.stop()
    server.stop()
    gps.stop()
    # TODO switch off the pi!
    if switch_off:
        pass
    os._exit(0)

def main():
    init()

    try:
        # Handy for debugging!
        # import code
        # code.interact(local=locals())
        while True:
            print "Gps data:"
            gps_data = gps.get_data()
            print gps_data
            db.set_current_gps_data(gps_data)
            time.sleep(DB_UPLOAD_INTERVAL)
    except (KeyboardInterrupt, SystemExit):
        print "Shutting down"
        shutdown()

if __name__ == '__main__':
    main()