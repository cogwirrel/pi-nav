import alexi.gps_reader as gps
import alexi.server as server
import time

def init():
    # Init logic goes here
    gps.start()
    server.start()

def shutdown():
    server.stop()
    gps.stop()

def main():
    init()

    try:
        # Handy for debugging!
        # import code
        # code.interact(local=locals())
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        shutdown()

if __name__ == '__main__':
    main()