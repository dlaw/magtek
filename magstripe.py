#!/usr/bin/python

import usb.core, usb.util

reader = usb.core.find(idVendor=0x0801, idProduct=0x0002)
if not reader: exit("MagTek card reader not found")
if reader.is_kernel_driver_active(0): reader.detach_kernel_driver(0)
reader.reset()
reader.set_configuration()
endpoint = reader[0][(0,0)][0]

def read():
    data = b''
    while True:
        try: data += endpoint.read(endpoint.wMaxPacketSize, 10)
        except usb.core.USBError as e:
            if 'Operation timed out' not in e.args or data: break
    if len(data) != 337: return [b'', b'', b'']
    return [data[7:][:data[3]], data[117:][:data[4]], data[227:][:data[5]]]

if __name__ == '__main__':
    for line in read():
        print(line.decode())
