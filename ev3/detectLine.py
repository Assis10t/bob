#! /usr/bin/env python3
import ev3dev.ev3 as ev3


class DetectLine:
    # Constructor
    def __init__(self):
        self.btn = ev3.Button()
        self.shut_down = False

    def run(self):
        cs = ev3.ColorSensor()
        assert cs.connected

        cs.mode = 'COL-REFLECT' # measure light intensity
        #cs.mode = 'COL-COLOR' # measure colour

        # motors
        flm = ev3.LargeMotor('outA')  # front-left motor
        frm = ev3.LargeMotor('outB')  # front-right motor
        sm = ev3.LargeMotor('outC')   # side motor
        #sm.run_timed(speed_sp=300, time_sp=1000)

        speed = 360 / 4  # deg/sec, [-1000, 1000]
        dt = 500  # milliseconds
        # stop_action = "coast"

        # PID tuning
        Kp = 1  # proportional gain
        Ki = 0  # integral gain
        Kd = 0  # derivative gain

        integral = 0
        previous_error = 0

        # initial measurement when using one sensor to callibrate
        target_value = cs.value()

        # Start the main loop
        while not self.shut_down:
            # Calculate steering using PID algorithm
            error = target_value - cs.value()
            integral += (error * dt)
            derivative = (error - previous_error) / dt

            # u zero:     on target,  drive forward
            # u positive: too bright, turn right
            # u negative: too dark,   turn left

            u = (Kp * error) + (Ki * integral) + (Kd * derivative)
            print(u)


# Main function
if __name__ == "__main__":
        robot = DetectLine()
        robot.run()