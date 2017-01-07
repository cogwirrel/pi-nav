import alexi.gps as gps

def main():
    gps.start()

    try:
        while True:
            print gps.get_data()
    except (KeyboardInterrupt, SystemExit):
        gps.stop()

if __name__ == '__main__':
    main()