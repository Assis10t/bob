#!/usr/bin/python3
from zeroconf import ServiceBrowser, Zeroconf
import requests
import socket
import struct

class MyListener:

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print(info.address.hex())
        print(info.port)
        str_ip =(socket.inet_ntoa(struct.pack(">L",int(info.address.hex(),16))))
        r = requests.get("http://{}:{}/ping".format(str_ip,info.port))
        print(r.text)




zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()
