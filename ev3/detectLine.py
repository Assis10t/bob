#! /usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep


class DetectLine:
    # From https://gist.github.com/CS2098/ecb3a078ed502c6a7d6e8d17dc095b48
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

        speed = 360 / 2.5   # deg/sec, [-1000, 1000]
        dt = 250  # milliseconds
        stop_action = "coast"

        # TODO: tune parameters, p then d then i (i will probably be very small)
        # PID tuning
        Kp = 2.5  # proportional gain   largest
        Ki = 0  # integral gain       medium
        Kd = 0.1  # derivative gain   lowest

        integral = 0
        previous_error = 0

        # initial measurement when using one sensor to callibrate
        # place sensor left half on white, right half on black
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

            # limit u to safe values: [-1000, 1000] deg/sec
            if speed + abs(u) > 1000:
                if u >= 0:
                    u = 1000 - speed
                else:
                    u = speed - 1000

            # run motors
            if u >= 0:
                # wheels are now at back so reverse motors
                frm.run_timed(time_sp=dt, speed_sp=-(speed + u))
                flm.run_timed(time_sp=dt, speed_sp=-(speed - u))
                sleep(dt / 1000)
            else:
                frm.run_timed(time_sp=dt, speed_sp=-(speed - u))
                flm.run_timed(time_sp=dt, speed_sp=-(speed + u))
                sleep(dt / 1000)

            previous_error = error

            # Check if buttons pressed (for pause or stop)
            if self.btn.down:  # Stop
                print("Exit program... ")
                self.shut_down = True
            elif self.btn.left:  # Pause
                print("[Pause]")
                self.pause()

            # 'Pause' method

    def pause(self, pct=0.0, adj=0.01):
        while self.btn.right or self.btn.left:  # ...wait 'right' button to unpause
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.AMBER, pct)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.AMBER, pct)
            if (pct + adj) < 0.0 or (pct + adj) > 1.0:
                adj = adj * -1.0
            pct = pct + adj

        print("[Continue]")
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)




# Main function
if __name__ == "__main__":
        robot = DetectLine()
        robot.run()