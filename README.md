# PI NAV
Navigation for Raspberry PI using a USB GPS dongle

## Setup
I don't know if this'll work for you, but I had to run the following to get data from my gps dongle.

### Setting up the Pi to read GPS from a dongle

This should all only need to be done once.

__Plug in your dongle__

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

### Building the UI

The UI can be found here: [pi-nav-ui](https://github.com/cogwirrel/pi-nav-ui)

Clone the repository in the same directory as `pi-nav`.

`cd pi-nav-ui`
`npm install`
`npm install -g gulp` <-- If you haven't got it already

Make sure you set up your own static/demo/credentials.js copied from the example.
See the [ffwdme.js](https://github.com/ffwdme/ffwdme.js) README for more info on credentials!

Once you're done, run this to build the UI!
`gulp build`

This populates the "static" folder in `pi-nav`.

### Building pi-nav

It's not really building but make sure you have the python requirements

`cd pi-nav`
`pip install -r requirements.txt`

## Running pi-nav

On your pi, run `start.sh` and watch the magic unfold!

