# PI NAV
## Navigation for Raspberry PI using USB GPS dongle

### Setup
I don't know if this'll work for you, but I had to run the following to get data from my gps.

This should be a one-time thing...

__Install gps stuff__
```
sudo apt-get update
sudo apt-get install gpsd gpsd-clients python-gps
```

__Disable gpsd service__
```
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
```

__Add to crontab (via `sudo crontab -e`)
```
# For listening to GPS
@reboot sudo stty -F /dev/ttyUSB0 4800
@reboot sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
```


