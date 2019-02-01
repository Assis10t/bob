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

        #cs.mode = 'COL-REFLECT' # measure light intensity
        cs.mode = 'COL-COLOR' # measure colour
        while(True):
            yeet = cs.value()
            print(yeet)

        # motors
        flm = ev3.LargeMotor('outA') # front-left motor
        frm = ev3.LargeMotor('outB') # front-right motor
        sm = ev3.LargeMotor('outC')  # sidemotor
        #sm.run_timed(speed_sp=300, time_sp=1000)


# Main function
if __name__ == "__main__":
        robot = detectLine()
        robot.run()