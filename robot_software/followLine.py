#! /usr/bin/env python3
import ev3dev.ev3 as ev3
import logging
from time import sleep, time
import control


class FollowLine:
    # From https://gist.github.com/CS2098/ecb3a078ed502c6a7d6e8d17dc095b48
    MOTOR_SPEED = 700
    DT = 50  # milliseconds  -  represents change in time since last sensor reading/

    MARKING_NUMBER = 2  # number of consecutive colour readings to detect marking
    MARKING_INTERVAL = 1  # time between marking checks in seconds
    REVERSE = False

    BLUE = 2  # blue reading from colour sensor in COL-COLOR mode
    GREEN = 3  # green reading from colour sensor in COL-COLOR mode

    # Constructor
    def __init__(self):
        self.btn = ev3.Button()
        self.shut_down = False

        # colour sensors
        self.csfl = ev3.ColorSensor('in1')  # colour sensor front left
        self.csfr = ev3.ColorSensor('in2')  # colour sensor front right
        self.csbl = ev3.ColorSensor('in3')  # colour sensor back left
        self.csbr = ev3.ColorSensor('in4')  # colour sensor back right
        assert self.csfl.connected
        assert self.csfr.connected
        assert self.csbl.connected
        assert self.csbr.connected

        # motors
        self.lm = ev3.LargeMotor('outA')  # left motor
        self.rm = ev3.LargeMotor('outC')  # right motor
        self.cm = ev3.LargeMotor('outD')  # centre motor
        assert self.lm.connected
        assert self.rm.connected
        assert self.cm.connected

        self.consecutive_colours = 0  # counter for consecutive colour readings
        self.ignore_blue = False  # when switching from sideways to forwards
        self.ignore_green = False  # when switching from fowards to sideways
        # self.number_of_markers = 0  # at which marker it should stop

    def detect_marking(self, colour_left, colour_right):
        print(colour_left, colour_right)
        if (colour_right == self.BLUE and colour_left == self.BLUE) \
                or (colour_right == self.GREEN and colour_left == self.GREEN):
            self.consecutive_colours += 1
            print("CONSECUTIVE COLOURS: ", self.consecutive_colours)
            if self.consecutive_colours > self.MARKING_NUMBER:
                return colour_right
        else:
            self.consecutive_colours = 0
        return -1

    # limit motor speed to safe values: [-1000, 1000] deg/sec
    @staticmethod
    def limit_speed(speed):
        if speed > 1000:
            return 1000
        if speed < -1000:
            return -1000
        return speed

    # adjust modes of colour sensors depending on the direction of Bob
    # COL-REFLECT: measure light intensity
    # COL-COLOR: measure colour
    def set_cs_modes(self, direction):
        if direction == 'forward':
            self.csfl.mode = 'COL-REFLECT'
            self.csfr.mode = 'COL-REFLECT'
            self.csbl.mode = 'COL-COLOR'
            self.csbr.mode = 'COL-COLOR'
        elif direction == 'backward':
            self.csfl.mode = 'COL-COLOR'
            self.csfr.mode = 'COL-COLOR'
            self.csbl.mode = 'COL-REFLECT'
            self.csbr.mode = 'COL-REFLECT'
        elif direction == 'left' or direction == 'right':
            self.csfl.mode = 'COL-COLOR'
            self.csfr.mode = 'COL-COLOR'
            self.csbl.mode = 'COL-COLOR'
            self.csbr.mode = 'COL-COLOR'
        else:
            return False  # wrong direction command sent
        return True


    # follows a line and corrects trajectory continually
    # uses light sensors to follow line and colour sensors to detect markings
    def correct_trajectory(self, number_of_markers, light_left, light_right, colour_left, colour_right, motor_left, motor_right):
        marker_counter = 0
        start_time = time()
        time_off_line = 0
        pid_controller = control.Control(self.DT)

        while not self.shut_down:
            # most likely off line, may need to recalibrate numbers later
            #time_off_line = self.get_back_on_line(light_left, light_right, time_off_line)

            # Calculate torque using PID control
            torque = pid_controller.calculate_torque(light_left.value(), light_right.value())
            # Set the speed of the motors
            speed_left = self.limit_speed(self.MOTOR_SPEED + torque)
            speed_right = self.limit_speed(self.MOTOR_SPEED - torque)

            # run motors
            motor_left.run_timed(time_sp=self.DT, speed_sp=-speed_left)
            motor_right.run_timed(time_sp=self.DT, speed_sp=-speed_right)
            sleep(self.DT / 1000)

            # Check markers
            # Wait before checking for colour again
            if time() - start_time > self.MARKING_INTERVAL:
                # returns 3 if green, 2 if blue
                marker_colour = self.detect_marking(colour_left, colour_right)
                #print(marker_colour)
                if marker_colour == self.GREEN:
                    # stop after given number of greens
                    self.ignore_blue = False
                    marker_counter += 1
                    ev3.Sound.beep()
                    start_time = time()
                    if marker_counter >= number_of_markers:
                        # self.stop()
                        return
                elif marker_colour == self.BLUE and not self.ignore_blue:
                    # stop on blue marker
                    # self.stop()
                    # self.reverse = not self.reverse
                    return

    def run_sideways(self, distance, reverse):
        self.ignore_blue = False

        # If previous instruction was forwards or backwards
        # keep moving until a blue line is seen
        if self.ignore_green:
            self.correct_trajectory(99, self.REVERSE)

        self.ignore_green = False

        if reverse:
            self.csfl.mode = 'COL-COLOR'  # measure light intensity
            self.csfr.mode = 'COL-REFLECT'  # measure colour
            self.csbl.mode = 'COL-COLOR'  # measure light intensity
            self.csbr.mode = 'COL-REFLECT'  # measure colour
        else:
            self.csfl.mode = 'COL-REFLECT'  # measure light intensity
            self.csfr.mode = 'COL-COLOR'  # measure colour
            self.csbl.mode = 'COL-REFLECT'  # measure light intensity
            self.csbr.mode = 'COL-COLOR'  # measure colour

        marker_counter = 0
        start_time = time()
        while not self.shut_down:
            if reverse:
                self.cm.run_timed(time_sp=self.DT / 2, speed_sp=-500)
            else:
                self.cm.run_timed(time_sp=self.DT / 2, speed_sp=500)
            sleep(self.DT / 2000)

            if time() - start_time > self.MARKING_INTERVAL:
                if reverse:
                    colour_left = self.csfl.value()
                    colour_right = self.csbl.value()
                else:
                    colour_left = self.csbr.value()
                    colour_right = self.csfr.value()

                # returns 3 if green, 2 if blue
                marker_colour = self.detect_marking(colour_left, colour_right)
                if marker_colour == self.BLUE:
                    # stop after given number of blues
                    marker_counter += 1
                    ev3.Sound.beep()
                    start_time = time()
                    if marker_counter >= distance:
                        # self.stop()
                        self.ignore_blue = True
                        return
                elif marker_colour == self.GREEN:
                    # stop on green marker
                    # self.stop()
                    # self.reverse = not self.reverse
                    return

    # move forward
    def run_forward(self, distance, direction):
        # set colour sensor modes and check if successful
        if self.set_cs_modes('forward'):
            # modes set successfully
            self.correct_trajectory(distance, self.csfl, self.csfr, self.csbl, self.csbr, self.lm, self.rm)
        else:
            # invalid direction string
            ev3.Sound.speak("Invalid direction:", direction).wait()
            # skipping execution of this command
            return

    def run_backward(self, distance, direction):
        # set colour sensor modes and check if successful
        if self.set_cs_modes('forward'):
            # modes set successfully
            self.correct_trajectory(distance, self.csbr, self.csbl, self.csfr, self.csfl, self.rm, self.lm)
        else:
            # invalid direction string
            ev3.Sound.speak("Invalid direction:", direction).wait()
            # skipping execution of this command
            return

    # when line is lost oscillate side to side until it is found
    def get_back_on_line(self, lval, rval, time_off_line):
        if lval > 90 and rval > 70:
            if time_off_line == 0:
                time_off_line = time()
            # if off line for more than a second move side-to-side until line is found
            print(time() - time_off_line)
            if time() - time_off_line > 0.5:
                correction_speed = 200
                correction_time = 100
                # can change thresholds
                while lval > 70 and rval > 50:
                    self.cm.run_timed(time_sp=correction_time, speed_sp=correction_speed)
                    correction_speed *= -1
                    # increase the time to move in one direction to increased the search radius
                    correction_time += 100
                    sleep(correction_time / 1000)  # milliseconds to seconds
                    lval = self.csfl.value()
                    rval = self.csfr.value()
                time_off_line = 0
        else:
            time_off_line = 0
        return time_off_line

    def stop(self):
        self.shut_down = True
        self.rm.stop()
        self.lm.stop()
        ev3.Sound.speak("bruh").wait()


# Main function
if __name__ == "__main__":
    robot = FollowLine()
