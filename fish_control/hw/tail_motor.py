"""
TailMotor – minimal wrapper around ROBOTIS Dynamixel SDK.
Works with U2D2 + power hub.
"""

from dynamixel_sdk import PortHandler, PacketHandler, COMM_SUCCESS

class TailMotor:
    PORT      = "/dev/ttyUSB0"
    BAUD      = 57600
    PROTOCOL  = 2.0
    ID        = 1

    # Control-table addresses for X-series:
    ADDR_TORQUE_ENABLE   = 64
    ADDR_OPERATING_MODE  = 11
    ADDR_GOAL_POSITION   = 116
    ADDR_PRESENT_POS     = 132
    ADDR_PRESENT_CURRENT = 126
    ADDR_PRESENT_VOLTAGE = 144

    def __init__(self):
        self.port   = PortHandler(self.PORT)
        self.packet = PacketHandler(self.PROTOCOL)
        if not self.port.openPort():
            raise RuntimeError("Cannot open " + self.PORT)
        self.port.setBaudRate(self.BAUD)
        if self.packet.ping(self.port, self.ID)[0] != COMM_SUCCESS:
            raise RuntimeError("Dynamixel ID 1 not responding")

        # config once
        self.packet.write1ByteTxRx(self.port, self.ID,
                                   self.ADDR_TORQUE_ENABLE, 0)   # torque off
        self.packet.write1ByteTxRx(self.port, self.ID,
                                   self.ADDR_OPERATING_MODE, 4)  # extended-pos
        self.packet.write1ByteTxRx(self.port, self.ID,
                                   self.ADDR_TORQUE_ENABLE, 1)

    # helpers ­-------------------------------------------
    @staticmethod
    def _deg_to_raw(deg: float) -> int:
        return int((deg / 360) * 4096)  # 0-360 → 0-4095

    def set_deg(self, deg: float):
        raw = self._deg_to_raw(deg)
        self.packet.write4ByteTxRx(self.port, self.ID,
                                   self.ADDR_GOAL_POSITION, raw)

    def state(self) -> dict:
        # readPresentPosition returns (comm_result, dxl_error, data)
        _, _, pos = self.packet.read4ByteTxRx(
            self.port, self.ID, self.ADDR_PRESENT_POS)
        _, _, cur = self.packet.read2ByteTxRx(
            self.port, self.ID, self.ADDR_PRESENT_CURRENT)
        _, _, volt = self.packet.read2ByteTxRx(
            self.port, self.ID, self.ADDR_PRESENT_VOLTAGE)

        return dict(
            pos_deg     = pos   * 360.0 / 4096.0,
            current_mA  = cur   * 2.69,
            voltage_V   = volt  * 0.1,
        )