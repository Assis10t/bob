#!/usr/bin/python3
import ev3dev.ev3 as ev3
from zeroconf import ServiceBrowser, Zeroconf
import requests
import socket
import struct
import time
from threading import Thread
from follow import FollowLine

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
            robot = FollowLine()
            robot.run()
            running = False
            continue
        time.sleep(2)

class MyListener:

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        ip_addr =(socket.inet_ntoa(info.address))
        port = info.port
        print(ip_addr,port,name)
        if (name == "assis10t._http._tcp.local."):
            r = requests.get("http://{}:{}/ping".format(ip_addr,port))
            # wait for r().esponse
            if (r.text == "pong"):
                print("Server running on {}:{}".format(ip_addr,port))
                ev3.Sound.tone([(1000, 250, 0),(1500, 250, 0),(2000, 250, 0)]).wait()
            else:
                print("Server did not respond!")
                ev3.Sound.tone([(750, 250, 0),(750, 250, 0)]).wait()
            poller = Thread(target=hello_world, name="poller",args=(ip_addr,port))
            poller.start()








ev3.Sound().beep().wait()
zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
try:

    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()
