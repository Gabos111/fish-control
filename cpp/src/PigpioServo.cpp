// PigpioServo.cpp  (daemon version)
#include "PigpioServo.h"
#include <pigpiod_if2.h>
#include <stdexcept>

PigpioServo::PigpioServo(int gpio)
    : gpio_pin(gpio)          // member-initialiser list
{
    pi = pigpio_start(nullptr, nullptr);   // connect to local pigpiod
    if (pi < 0)
        throw std::runtime_error("pigpio_start failed");
    setAngle(90);
}

PigpioServo::~PigpioServo()
{
    if (pi >= 0)
        pigpio_stop(pi);
}

void PigpioServo::setAngle(double deg)
{
    double pulse = 500 + (deg / 180.0) * 2000;  // µs
    set_servo_pulsewidth(pi, gpio_pin, pulse);
}