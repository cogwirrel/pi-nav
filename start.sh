#!/bin/bash

# Change 4800 to your GPS dongle's baud rate if it's different
sudo stty -F /dev/ttyUSB0 4800

sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock

python src/main.py