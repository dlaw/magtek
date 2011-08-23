#!/usr/bin/python

import sys, usb.core, usb.util

device = usb.core.find(idVendor=0x0801, idProduct=0x0002)
if not device: sys.exit("Could not find MagTek card reader")
try:
    if device.is_kernel_driver_active(0):
        device.detach_kernel_driver(0)
    device.reset()
    device.set_configuration()
except usb.core.USBError:
    sys.exit("Could not set up MagTek card reader")
endpoint = device[0][(0,0)][0]

def read():
    data = b''
    while True:
        try: data += endpoint.read(endpoint.wMaxPacketSize, 10)
        except usb.core.USBError as e:
            if 'Operation timed out' not in e.args or data:
                break
    if len(data) != 337: return [b'', b'', b'']
    tracks = []
    for track_length_index, track_start in [(3,7), (4,117), (5,227)]:
        tracks.append(data[track_start:][:data[track_length_index]])
    return tracks

if __name__ == '__main__':
    for line in read():
        print(line.decode())
