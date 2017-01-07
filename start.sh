#!/bin/bash

sudo stty -F /dev/ttyUSB0 4800
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock

python src/main.py