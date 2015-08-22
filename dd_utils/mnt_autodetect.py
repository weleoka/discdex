#!/usr/bin/env python3
# Courtesy of:
# http://stackoverflow.com/questions/22615750/how-can-the-directory-of-a-usb-drive-connected-to-a-system-be-obtained
import os
from glob import glob
from subprocess import check_output, CalledProcessError

def get_usb_devices():
    sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
    usb_devices = (dev for dev in sdb_devices
        if 'usb' in dev.split('/')[5])
    # for dev in sdb_devices:
        # print (os.path.basename(dev), dev)
    return dict((os.path.basename(dev), dev) for dev in usb_devices)

def get_mount_points(devices=None):
    devices = devices or get_usb_devices() # if devices are None: get_usb_devices
    output = check_output(['mount']).splitlines()
    is_usb = lambda path: any(dev in path for dev in devices)
    usb_info = (line for line in output if is_usb(line.decode().split()[0]))    #python3 needs to decode to str.
    return [(info.split()[0], info.split()[2]) for info in usb_info]

if __name__ == '__main__':
    print (get_mount_points())