"""
FinServo – RC-servo via pigpio (needs pigpiod running)
"""

import pigpio

class FinServo:
    SERVO_PIN = 18
    MIN_PW = 500     # µs at 0°
    MAX_PW = 2500    # µs at 180°

    def __init__(self):
        self.gpio = pigpio.pi()
        if not self.gpio.connected:
            raise RuntimeError("pigpiod not running")
        self.set_deg(90)   # neutral

    def set_deg(self, deg: float):
        deg = max(0, min(180, deg))
        pw = self.MIN_PW + (deg / 180) * (self.MAX_PW - self.MIN_PW)
        self.gpio.set_servo_pulsewidth(self.SERVO_PIN, pw)

    def stop(self):
        self.gpio.set_servo_pulsewidth(self.SERVO_PIN, 0)
        self.gpio.stop()