# PI NAV
Navigation for Raspberry PI using a USB GPS dongle.

This project is designed to be set up in a car, and it's intended use has the following hardware:
- 3G or 4G wifi - I'm using a [telstra one](https://www.telstra.com.au/mobile-phones/prepaid-mobiles/telstra-pre-paid-4gx-wi-fi-with-car-kit#)
- Raspberry Pi - I'm using the Pi 3, model B
- Gps dongle - I'm using a [Haicom HI-206 USB](http://www.haicom.com.tw/GPS_Receivers/HI-206USB/Product.aspx)
- Amazon Echo Dot
- A screen of some kind in your car - I'm using a [JVC KW-AV61BT](http://support.jvc.com/consumer/product.jsp?modelId=MODL029190)

Using all of these cool things together means voice control sattelite navigation for your car!

The project consists of three repositories:
- pi-nav (this one!)
- pi-nav-ui (the user interface for pi-nav)
- pi-nav-lambda (AWS lambda function for Alexa skill)

The UI is a fork of a seriously cool project called [ffwdme.js](https://ffwdmejs.org/) - worth checking out!

## Setup

### Setting up the Pi to read GPS from a dongle

I had to do the following setup to get data from my gps dongle - do whatever works for you!

This should all only need to be done once.

__Plug in your dongle__

__Install gps stuff__
```
sudo apt-get update
sudo apt-get install gpsd gpsd-clients python-gps
```

__Edit `/etc/default/gpsd` config so it doesn't auto-start__
```
# Start the gpsd daemon automatically at boot time
START_DAEMON="false"

# Use USB hotplugging to add new USB devices automatically to the daemon
USBAUTO="false"
```

### Building the UI

Building doesn't work on the pi, so please do this on another computer.

Clone this repository and [`pi-nav-ui`](https://github.com/cogwirrel/pi-nav-ui) repository in the same directory.

`cd pi-nav-ui`
`npm install`
`npm install -g gulp`

Make sure you set up your own `static/demo/credentials.js` copied from the example.
See the [ffwdme.js](https://github.com/ffwdme/ffwdme.js) README for more info on credentials!

Once you're done, run this to build the UI!
`gulp build`

This populates the "static" folder in `pi-nav`.

### Building pi-nav

It's not really building but make sure you have the python requirements

`cd pi-nav`
`sudo pip install -r requirements.txt`

## Setting up your IoT credentials

Set up credentials in the usual way on the AWS IoT console

Download all the files and paste the appropriate ones in the `.example` files, and remove the `.example` extension

Edit `config.py.example` to point to your endpoint which can also be found on the AWS IoT console, and remove the `.example` extension

## Running pi-nav

Copy everything onto your pi, eg:

`scp -r pi-nav pi@<YOUR_PI_IP_ADDRESS>:/home/pi/pi-nav`

On your pi:

```
cd /home/pi/pi-nav
./start.sh
```

You can exit the UI with Ctrl-W, and kill the server in the terminal with Ctrl-C

## Building pi-nav-lambda

Use `./build.sh` to zip up all the source into `output/lambda_function.zip`

Upload to lambda with `./upload.sh` (you'll want to modify it and set up your AWS credentials first though!)

