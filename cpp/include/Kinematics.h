#pragma once

// Convert a fin deflection phi (rad) to servo angle (deg)
double fin_to_servo(double phi);

// Solve inverse tail kinematics: given tail angle phi (deg), return motor angle theta (deg)
double inverse_tail(double phi);