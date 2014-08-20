# Simple Newport USB Driver wrapper for python using ctypes.
# Tested with a Newfocus TLB 6712B tunable laser.
#
# Copyright (c) 2014 Callum Doolin (doolin@ualberta.ca)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import ctypes
from exceptions import RuntimeError
import atexit
from collections import namedtuple

# let's not load the newpdll on import, so programs won't break
# immediately if the dll isn't present.  It will only break when
# actually doing something with the library.
newpdll = None


def init():
    if init.ed:
        return
        
    # load dll and initialize USB address devices
    global newpdll
    newpdll = ctypes.oledll.LoadLibrary("usbdll.dll")
    newpdll.newp_usb_init_system()
    
    init.ed = True
    atexit.register(uninit)
init.ed = False

def uninit():
    if init.ed:
        newpdll.newp_usb_uninit_system()
        init.ed = False
    
USBAddress = namedtuple("USBAddress", ['id', 'info'])

def get_addresses():
    init()
    # and get a list of all the devices
    devinfo = ctypes.create_string_buffer(1024)
    newpdll.newp_usb_get_device_info(devinfo)
    
    adds = []
    for dev in devinfo.value.split(";"):
        splitted = dev.split(',')
        if len(splitted) > 1:
            id = int(splitted[0])
            if id < 1 or id > 31:
                raise RuntimeError("Invalid device id found (%d)" % id)
            adds.append(USBAddress(id=id, info=splitted[1]))
    return adds


class Device(object):
    def __init__(self, address=None):
        # load dll if needed
        init()
        self.last = ""
        
        # if no address specified, find first device automatically
        if address is None:
            addresses = get_addresses()
            if len(addresses) > 0:
                address = addresses[0]
            else:
                raise RuntimeError("No laser connected")

        # assume address is a USBAddress object, otherwise treat as
        # the device ID
        try:
            id = address.id
        except AttributeError:
            try:
                id = int(address)
            except (TypeError, ValueError):
                raise TypeError("Expected a USBAddress or int for address")

        self.devid = ctypes.c_long(id)
        self.buff = ctypes.create_string_buffer(64);
        self.n = ctypes.c_ulong(0)
        self.verbose = False

    def ask(self, q):
        # sends message q to newport device and returns the reply.
        # must use create_string_buffer or python will crash.
        c_q = ctypes.create_string_buffer(q)
        err = newpdll.newp_usb_send_ascii(
            self.devid, c_q, ctypes.c_ulong(len(q)))
        if err != 0:
            raise RuntimeError("Error %d sending \"%s\" to newport usb"
                % (err, q))

        err = newpdll.newp_usb_get_ascii(
            self.devid, self.buff, ctypes.c_ulong(64), ctypes.byref(self.n))
        if err != 0:
            raise RuntimeError(
                "Error %d receiving message from newport usb" % err)
        reply = self.buff.value
        
        # the bytes returned paramater doesn't seem to work,  so look for
        # a line feed or carriage return + line feed
        end = reply.find("\n")
        if end is -1:
            # no newline found
            pass
        elif reply[end-1] == "\r":
            # return up to carriage return
            reply =  reply[:end-1]
        else:
            # return up to line feed
            reply = reply[:end]

        if self.verbose:
            print("%s -> %s" % (q, reply))

        return reply


if __name__ == "__main__":
    d = Device()
    
    import IPython
    IPython.embed()
