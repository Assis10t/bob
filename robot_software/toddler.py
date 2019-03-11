import time
import numpy
import cv2
import sys
import os
import socket
from threading import Thread
from iotools import IOTools
from grabber import Grabber


class Logger(object):
    def __init__(self, onRobot):
        self.useTerminal = not onRobot
        self.terminal = sys.stdout
        self.log = 0
        if os.path.isdir('/tmp/sandbox'):
            self.log = open('/tmp/sandbox/log.txt', 'a+')

    def write(self, message):
        if self.useTerminal:
            self.terminal.write(message)
        if self.log:
            self.log.write(message)
            self.log.flush()

    def flush(self):
        pass


class Toddler:

    MOTOR_PORT = 1

    def __init__(self, onRobot):
        IO = IOTools(onRobot)
        print('Grabber initialised')
        self.camera = IO.camera.initCamera('pi', 'low')
        self.getInputs = IO.interface_kit.getInputs
        self.getSensors = IO.interface_kit.getSensors
        self.mc = IO.motor_control
        self.sc = IO.servo_control
        self.grabber = Grabber(self.mc, self.MOTOR_PORT, self.sc)
        #self.mc.setMotor(self.MOTOR_PORT, 100)
        #time.sleep(3)
        #self.mc.stopMotors()

    def listen():
        PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = socket.gethostbyname(socket.gethostname())
        s.bind((HOST, PORT))
        print("Listening on {}:{}".format(HOST, PORT))
        while True:
            s.listen(1)
            conn, addr = s.accept()

            print('Connected by', addr)

            data = conn.recv(1024)
            if data == b'grab':
                self.grabber.grab()
            elif data == b'prepare':
                self.grabber.prepare_grabber()
            conn.sendall(b'done')
            conn.close()

    def control(self):
        try:
            thread = Thread(target=self.listen)
            thread.start()

            # start pinging the server
            # server, rasppi, ev3


        except KeyboardInterrupt:
            return

    def vision(self):
        # image = self.camera.getFrame()
        # self.camera.imshow('Camera', image)
        time.sleep(0.05)
        return


if __name__ == '__main__':
    onRobot = bool(sys.argv.count('-rss'))
    sys.stdout = Logger(onRobot)
    sys.stderr = sys.stdout
    t = Toddler(onRobot)
    try:
        while 1:
            t.listen()
    except KeyboardInterrupt:
        print("stop")


