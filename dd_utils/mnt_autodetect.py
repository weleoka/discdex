#!/usr/bin/env python3
"""
Utility module for Discdex.
Module which contains functions which access the filesystem and checks for mounted devices.

Partly courtesy of:
http://stackoverflow.com/questions/22615750/how-can-the-directory-of-a-usb-drive-connected-to-a-system-be-obtained
"""

import os
from glob import glob
from subprocess import check_output, CalledProcessError


def get_usb_devices():
    """
    Check for USB mounted file systems.

    parameters:
       
    return:
        string. Path to USB file system.
        
    """
    sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
    usb_devices = (dev for dev in sdb_devices
        if 'usb' in dev.split('/')[5])
    # for dev in sdb_devices:
       # print ("aa: %s, bb: %s"
          #  % (os.path.basename(dev), dev))

    return dict((os.path.basename(dev), dev) for dev in usb_devices)


def get_mounted_filesystems():
    """
    Check for mounted fie systems and return path to device.

    parameters:
       
    return:
        String. Path to mounted file system.
        
    """
    sdb_devices = map(os.path.realpath, glob('/sys/block/s*'))
    rem_devices = (dev for dev in sdb_devices if 'usb' or 'sr0' in dev.split('/')[5])
    #for dev in sdb_devices:
      #  print ("aa: %s, bb: %s"
        #    % (os.path.basename(dev), dev))

    return dict((os.path.basename(dev), dev) for dev in rem_devices)


def get_mount_points(devices=None):
    """
    Description

    parameters:
       
    return:
        
    """
    devices = devices or get_mounted_filesystems() # if devices are None: get_mounted_filesystems
    output = check_output(['mount']).splitlines()
    is_usb = lambda path: any(dev in path for dev in devices)
    usb_info = (line for line in output if is_usb(line.decode().split()[0]))    #python3 needs to decode to str.

    return [(info.split()[0], info.split()[2]) for info in usb_info]

if __name__ == '__main__':
    print (get_mount_points())