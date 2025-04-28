"""
Fish kinematics helpers (pure Python, no compile step)
"""

import math

def fin_to_servo(phi: float) -> float:
    """Physical fin angle φ (deg) -> RC-servo command θ (deg)."""
    theta = ((phi - 0.070) / 1.091) + 90.0
    return max(0.0, min(180.0, theta))

def _tail_func(theta: float) -> float:
    """Polynomial from TailKinematics.cpp  θ(deg)->φ(deg)."""
    return (
        5.77e-8 * theta**4
        - 4.303e-5 * theta**3
        - 2.631e-5 * theta**2
        + 1.045 * theta
        + 0.2932
    )

def inverse_tail(phi: float, tol: float = 0.1) -> float:
    """Binary-search φ = f(θ) for θ ∈ [0,90]."""
    lo, hi = 0.0, 90.0
    if phi <= _tail_func(lo):
        return lo
    if phi >= _tail_func(hi):
        return hi
    for _ in range(25):
        mid = (lo + hi) / 2
        if abs(_tail_func(mid) - phi) < tol:
            return mid
        if _tail_func(mid) < phi:
            lo = mid
        else:
            hi = mid
    return mid