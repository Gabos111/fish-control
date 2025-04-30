#pragma once
#include <stdexcept>

/** Simple wrapper around pigpiod’s servo control */
class PigpioServo
{
public:
    explicit PigpioServo(int gpio);   // BCM pin
    ~PigpioServo();

    void setAngle(double deg);        // 0-180°

private:
    int pi        = -1;   // connection handle from pigpio_start()
    int gpio_pin  = -1;   // saved pin number
};