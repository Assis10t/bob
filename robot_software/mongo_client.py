#!/usr/bin/python3

#check that the robot packages are present
ev3_package_check = True
try:
    import ev3dev.ev3 as ev3
    from follow import FollowLine
except:
    print("Unable to load robot control packages package!")
    ev3_package_check = False

import requests
import socket
import struct
import time
import sys
import datetime
from threading import Thread
from zeroconf import ServiceBrowser, Zeroconf


last_json = {}

def polling(ip_addr, port, run_robot):
    r = requests.get("http://{}:{}/jobs".format(ip_addr,port))
    last_json = r.text
    running = True
    while running:
        try:
            r = requests.get("http://{}:{}/jobs".format(ip_addr,port))
            if (r.text != last_json):
                #fire motors
                print("JSON CHANGED!")
                if (run_robot):
                    robot = FollowLine()
                    robot.run()
                    # TODO: Find out a way to halt this call 
                    # so we can start and stop the robot
                running = False
                continue
        except: 
            url = "http://{}:{}/jobs".format(ip_addr,port)
            print("GET request: {} failed at {}".format(url,datetime.datetime.now()))
        time.sleep(2)

class MyListener:
    def __init__(self,run_robot):
        self.run_robot = run_robot
    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        ip_addr =(socket.inet_ntoa(info.address))
        port = info.port
        print(ip_addr,port,name)
        if (name == "assis10t._http._tcp.local."):
            r = requests.get("http://{}:{}/ping".format(ip_addr,port))
            # wait for response
            if (r.text == "pong"):
                print("Server running on {}:{}".format(ip_addr,port))
                if (self.run_robot):
                    ev3.Sound.tone([(1000, 250, 0),(1500, 250, 0),(2000, 250, 0)]).wait()
                    # TODO: add light to indicate status
                poller = Thread(target=polling, name="poller",args=(ip_addr,port,self.run_robot))
                poller.start()
            else:
                print("Server did not respond!")
                if (self.run_robot):
                    ev3.Sound.tone([(750, 250, 0),(750, 250, 0)]).wait()
                    # TODO: add light to indicate status
           





if __name__ == "__main__":
    run_robot = None
    if (len(sys.argv) > 1):
        mode_str = sys.argv[1]
        #TODO: clean this up
        if (mode_str == 'r' or mode_str == 'robot' and ev3_package_present == True):
            ev3.Sound().beep().wait()
            run_robot = True
        elif (mode_str == "t" or mode_str=="test"):
            print("Running client in test mode...")
            print(''.join(['-' for x in range(40)]) + '\n')
            run_robot = False
        else:
            print('Unable to determine mode! r/robot -> robot | t/test -> test')
            exit()
    else:
        if (ev3_package_check):
            #assume robot mode
            run_robot = True
        else:
            print("Unable to start client as ev3 package not present and test mode not indicated")
            exit()
    zeroconf = Zeroconf()
    listener = MyListener(run_robot)
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
    try:

        input("Press enter to exit...\n\n")
    finally:
        zeroconf.close()
    
