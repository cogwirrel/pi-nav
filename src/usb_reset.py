#!/usr/bin/env python

# Modified version of http://superuser.com/questions/572034/how-to-restart-ttyusb
import os
import sys
from subprocess import Popen, PIPE
import fcntl

USBDEVFS_RESET= 21780

try:

    lsmod_out = Popen("lsmod | grep -i usbserial", shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, close_fds=True).stdout.read().strip().split()

    driver = lsmod_out[-1]
    print "Found usbserial driver: {}".format(driver)

    lsusb_out = Popen("lsusb | grep -i %s"%driver, shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, close_fds=True).stdout.read().strip().split()

    bus = lsusb_out[1]
    device = lsusb_out[3][:-1]

    driver_path = "/dev/bus/usb/{}/{}".format(bus, device)

    print "Resetting driver at: {}".format(driver_path)
    f = open(driver_path, 'w', os.O_WRONLY)
    fcntl.ioctl(f, USBDEVFS_RESET, 0)
    f.close()
except Exception, msg:
    print "Failed to reset device:", msg