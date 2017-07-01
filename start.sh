#!/bin/bash

# Default args
NO_UI=false
NO_KIOSK=false
NEW_UI_SESSION=false

# Argument parsing!
ARGS=`getopt -o '' -l no-ui,no-kiosk,new-ui-session -- "$@"`

eval set -- "$ARGS"

while true ; do
    case "$1" in
        --no-ui) NO_UI=true; shift 1;;
        --no-kiosk) NO_KIOSK=true; shift 1;;
        --new-ui-session) NEW_UI_SESSION=true; shift 1;;
        --) shift; break;;
    esac
done

# Redirect USB audio in to speakers!
echo "Piping sound from AUX to speakers"
arecord -D sysdefault:CARD=1 -f dat | aplay -f dat -B 100000 &

# Change to where you put pi-nav
pushd /home/pi/pi-nav/

# Ugly but gpsd is flakey so it's best to kill it first!
echo "Killing any gpsd that might be running"
sudo killall gpsd
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
sleep 1

# Change 4800 to your GPS dongle's baud rate if it's different
echo "Setting baud rate to 4800"
sudo stty -F /dev/ttyUSB0 4800
sleep 1

# Unplug and plug back in the usb, because the driver is flaky
echo "Unplugging and plugging in USB"
sudo python src/usb_reset.py
sleep 2

# Wait until we've read a byte from the gps
echo "Waiting to read a byte from the gps!"
sudo dd if=/dev/ttyUSB0 bs=1 count=1

echo "Starting up a gpsd socket"
sudo gpsd -n /dev/ttyUSB0 -F /var/run/gpsd.sock
sleep 1

echo "Starting server"
python src/main.py &

# Run in incognito mode so it doesn't complain about restoring pages
BROWSER_ARGS="--incognito"

if [ $NO_KIOSK == false ]; then
    echo "Disabling kiosk mode"
    BROWSER_ARGS="--kiosk $BROWSER_ARGS"
fi

if [ $NEW_UI_SESSION == true ]; then
    echo "UI in new session"
    BROWSER_ARGS="--temp-profile $BROWSER_ARGS"
fi

BROWSER_ARGS="$BROWSER_ARGS http://127.0.0.1:5555"
if [ $NO_UI == false ]; then
    echo "Starting user interface"
    chromium-browser $BROWSER_ARGS
fi

popd