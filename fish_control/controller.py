"""
Controller that implements 3 modes:
• standby         – torque off, fins neutral
• test            – hold target angles from cfg.yaml (phi_tail/phi_fin)
• symmetric_sin   – sinusoid using amplitude + frequency
"""

import math, time
from collections import deque
from .kinematics import inverse_tail, fin_to_servo
from .config     import get_cfg
from .hw.tail_motor import TailMotor
from .hw.fin_servo  import FinServo
from .logger    import CSVLogger

class FishController:
    LOOP_DT = 0.05   # 20 Hz

    def __init__(self):
        self.tail = TailMotor()
        self.fin  = FinServo()
        self.log = None
        self.logging_prev = False
        self.log_buffer = deque()
        self.last_flush = 0.0
        self.t0   = time.time()

    # ------------------------------------------------------------------
    def run(self):
        try:
            while True:
                t = time.time() - self.t0
                cfg = get_cfg()
                logging_on = cfg.get("logging", False)
                if logging_on and not self.logging_prev:
                    self.log = CSVLogger()    # turned on → create new log file
                elif not logging_on and self.logging_prev:
                    self.log = None           # turned off → drop the logger
                    self.logging_prev = logging_on

                mode = cfg.get("mode", "standby")

                if mode == "standby":
                    self.tail.set_deg(0)
                    self.fin.set_deg(90)
                    phi_tail = phi_fin = 0

                elif mode == "test":
                    phi_tail = cfg.get("phi_tail", 0.0)
                    phi_fin  = cfg.get("phi_fin", 0.0)

                else:  # symmetric_sin
                    A_t = cfg.get("amplitude_tail", 20)
                    A_f = cfg.get("amplitude_fin" , 15)
                    f   = cfg.get("frequency", 0.5)
                    ph  = cfg.get("phase", 0.0)
                    phi_tail = A_t * math.sin(2*math.pi*f*t)
                    phi_fin  = A_f * math.sin(2*math.pi*f*t + ph)

                theta_tail = inverse_tail(phi_tail)
                theta_fin  = fin_to_servo(phi_fin)

                self.tail.set_deg(theta_tail)
                self.fin .set_deg(theta_fin)

                state = self.tail.state()
                if self.log:
                    # buffer the row
                    self.log_buffer.append((
                        t,
                        phi_tail, theta_tail,
                        phi_fin,  theta_fin,
                        state["pos_deg"],
                        state["current_mA"],
                        state["voltage_V"],
                        mode.upper()
                    ))
                    # flush buffer once a second
                    if t - self.last_flush >= 1.0:
                        while self.log_buffer:
                            self.log.row(*self.log_buffer.popleft())
                        self.last_flush = t

                time.sleep(self.LOOP_DT)

        except KeyboardInterrupt:
            print("Stopping…")
        finally:
            self.tail.set_deg(0)
            self.fin.stop()