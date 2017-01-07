# PI NAV
## Navigation for Raspberry PI using USB GPS dongle

### Setup
I don't know if this'll work for you, but I had to run the following to get data from my gps dongle.

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

__Edit `/etc/default/gpsd` config so it looks like this__
```
# Start the gpsd daemon automatically at boot time
START_DAEMON="false"

# Use USB hotplugging to add new USB devices automatically to the daemon
USBAUTO="true"

# Devices gpsd should collect to at boot time.
# They need to be read/writeable, either by user gpsd or the group dialout.
DEVICES="/dev/ttyUSB0"

# Other options you want to pass to gpsd
GPSD_OPTIONS=""

GPSD_SOCKET="/var/run/gpsd.sock"
```


