#! /usr/bin/env python3
import ev3dev.ev3 as ev3

class detectLine:
    # Constructor
    def __init__(self):
        self.btn = ev3.Button()
        self.shut_down = False

    def run(self):
        cs = ev3.ColorSensor()
        assert cs.connected

        cs.mode = 'COL-REFLECT' # measure light intensity

        # motors
        flm = ev3.LargeMotor('outA') # forward-left motor
        frm = ev3.LargeMotor('outB') # forward-right motor
        sm = ev3.LargeMotor('outC')  # sidemotor
        sm.run_timed(speed_sp=300, time_sp=1000)