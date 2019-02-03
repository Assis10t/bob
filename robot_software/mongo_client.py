#!/usr/bin/python3
from zeroconf import ServiceBrowser, Zeroconf
import requests
import socket
import struct
import time
from threading import Thread

last_json = {}

def hello_world(ip_addr, port):
    r = requests.get("http://{}:{}/jobs".format(ip_addr,port))
    last_json = r.text
    running = True
    while running:
        r = requests.get("http://{}:{}/jobs".format(ip_addr,port))
        if (r.text != last_json):
            #fire motors
            print("JSON CHANGED!")
            running = False
            continue
        time.sleep(2)

class MyListener:

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print(info.address.hex())
        print(info.port)
        ip_addr =(socket.inet_ntoa(struct.pack(">L",int(info.address.hex(),16))))
        port = info.port
        r = requests.get("http://{}:{}/ping".format(ip_addr,port))
        # wait for response
        if (r.text == "pong"):
            print("Server running on {}:{}".format(ip_addr,port))
        else:
            print("Server did not respond!")
        poller = Thread(target=hello_world, name="poller",args=(ip_addr,port))
        poller.start()
        
        





zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
try:
   
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()
