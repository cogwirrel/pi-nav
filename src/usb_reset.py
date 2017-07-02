#!/usr/bin/env python

# Modified version of http://superuser.com/questions/572034/how-to-restart-ttyusb

# This resets the GPS usb, named ttyNAV (see README.md for how to name it this!)

import os
import sys
from subprocess import Popen, PIPE
import fcntl

USBDEVFS_RESET = 21780

def cmd(command):
    return Popen(command, shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, close_fds=True).stdout.read().strip().split('\n')


def dev_num(tty):
    search = "ATTRS{devnum}=="
    return cmd('udevadm info -a -n {} | grep "{}" | head -n1'.format(tty, search))[0].split('"')[1].zfill(3)

try:
    lsmod_out = cmd("lsmod | grep -i usbserial")[0].split()
    print "lsmod_out"
    print lsmod_out

    driver = lsmod_out[-1]
    print "Found usbserial driver: {}".format(driver)

    device = dev_num('/dev/ttyNAV')
    print "Got device number for /dev/ttyNAV: {}".format(device)

    lsusb_out = cmd("lsusb | grep -i {} | grep {}".format(driver, device))[0].split()
    print "lsusb_out"
    print lsusb_out

    bus = lsusb_out[1]
    device = lsusb_out[3][:-1]

    driver_path = "/dev/bus/usb/{}/{}".format(bus, device)

    print "Resetting driver at: {}".format(driver_path)

    f = open(driver_path, 'w', os.O_WRONLY)
    fcntl.ioctl(f, USBDEVFS_RESET, 0)
    f.close()
except Exception, msg:
    print "Failed to reset device:", msg
