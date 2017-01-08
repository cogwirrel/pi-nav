import alexi.gps_reader as gps
import alexi.server as server
import alexi.iot.iot as iot
import time
import os

def init():
    # Init logic goes here
    gps.start()
    server.start()
    iot.start()

def shutdown():
    iot.stop()
    server.stop()
    gps.stop()

def main():
    init()

    try:
        # Handy for debugging!
        # import code
        # code.interact(local=locals())
        while True:
            print "Gps data:"
            print gps.get_data()
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        print "Shutting down"
        shutdown()
        os._exit(0)

if __name__ == '__main__':
    main()