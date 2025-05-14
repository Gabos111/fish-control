#include "Kinematics.h"
#include <cmath>

// Linear mapping from fin deflection to servo PWM angle
double fin_to_servo(double phi) {

    float gear_ratio = 21.0/26.0; // gear ratio (servo-gear)
    float r_servo_pulley = 7.25; // radius of servo pulley (mm)
    float r_fin_pulley = 17.5; // radius of fin pulley (mm)
    float k = gear_ratio*(r_servo_pulley/r_fin_pulley); // transmission ratio (servo-gear-pulley)
    double theta = phi/k + 90.0;

    if (theta < 0.0) 
        theta = 0.0;
    if (theta > 180) 
        theta = 180.0;

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