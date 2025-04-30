#include "Kinematics.h"
#include <cmath>

// Linear mapping from fin deflection to servo PWM angle
double fin_to_servo(double phi) {
    // Linear calibration derived experimentally (Arduino reference):
    // servoAngle[deg] = ((phi[rad] - 0.070) / 1.091) + 90
    double theta = ((phi - 0.070) / 1.091) + 90.0;
    if (theta < 0.0)   theta = 0.0;
    if (theta > 180.0) theta = 180.0;
    return theta;
}

// Tail kinematics function f(theta)
static double tail_f(double theta) {
    return 5.77e-08*pow(theta,4)
         - 4.303e-05*pow(theta,3)
         - 2.631e-05*pow(theta,2)
         + 1.045*theta + 0.2932;
}

double inverse_tail(double phi)
{
    double sign = (phi < 0) ? -1.0 : 1.0;
    phi = std::abs(phi);

    double low = 0.0, high = 90.0;
    if (phi < tail_f(low))  return 0.0;
    if (phi > tail_f(high)) return sign * high;

    double mid{};
    for (int i = 0; i < 30; ++i)
    {
        mid = 0.5 * (low + high);
        double fm = tail_f(mid);
        if (std::fabs(fm - phi) < 0.01) break;
        (fm < phi ? low : high) = mid;
    }
    return sign * mid;
}