import alexi.gps_reader as gps
import time

def main():
    gps.start()

    try:
        while True:
            print gps.get_data()
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        gps.stop()

if __name__ == '__main__':
    main()