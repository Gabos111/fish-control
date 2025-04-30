#include "DynamixelSDKWrapper.h"
#include <dynamixel_sdk/dynamixel_sdk.h>
#include <string>
#include <stdexcept>
using namespace dynamixel;

// protocol version for DYNAMIXELs
static constexpr double PROTOCOL_VERSION = 2.0;

// Control‐table addresses (MX/XL / adjust if needed)
static constexpr uint16_t ADDR_GOAL_POSITION        = 116;
static constexpr uint16_t ADDR_PRESENT_POSITION     = 132;
static constexpr uint16_t ADDR_PRESENT_CURRENT      = 126;
static constexpr uint16_t ADDR_PRESENT_INPUT_VOLTAGE = 144;

DynamixelSDKWrapper::DynamixelSDKWrapper(const std::string& port,
                                         int baud,
                                         uint8_t id)
  : portHandler_(PortHandler::getPortHandler(port.c_str())),
    packetHandler_(PacketHandler::getPacketHandler(2.0)),
    id_(id),
    bulkRead_(portHandler_,packetHandler_)
{
  if (!portHandler_->openPort())
    throw std::runtime_error("Failed to open port");
  if (!portHandler_->setBaudRate(baud))
    throw std::runtime_error("Failed to set baudrate");

  // Sanity check : Dynamixel Ping
    {
      uint8_t dxl_error = 0;
      // ping returns COMM_SUCCESS (0) on success
      int dxl_comm_result = packetHandler_->ping(
        portHandler_,        // PortHandler*
        id_,                 // Dynamixel ID
        nullptr,             // pointer to model number (we don’t need it)
        &dxl_error           // pointer to error status
      );
      if (dxl_comm_result != COMM_SUCCESS) {
        throw std::runtime_error(
          "Dynamixel ping failed: " +
          std::string(packetHandler_->getTxRxResult(dxl_comm_result))
        );
      }
    }

  // --- make sure the actuator is ready to move -----------------------------
  {
      uint8_t dxl_error = 0;
      const uint16_t ADDR_TORQUE_ENABLE = 64;
      int rc = packetHandler_->write1ByteTxRx(
                  portHandler_, id_, ADDR_TORQUE_ENABLE, 1, &dxl_error);
      if (rc != COMM_SUCCESS || dxl_error)
      {
          throw std::runtime_error(
              "Failed to enable torque: " +
              std::string(packetHandler_->getTxRxResult(rc)) +
              " / err=" + std::to_string(dxl_error));
      }
  }

  // Register registers for one-shot reading
  bulkRead_.addParam(id_,ADDR_PRESENT_POSITION,     4);
  bulkRead_.addParam(id_, ADDR_PRESENT_CURRENT,      2);
  bulkRead_.addParam(id_, ADDR_PRESENT_INPUT_VOLTAGE,1);
}

void DynamixelSDKWrapper::setPositionDeg(double deg) {
    uint8_t dxl_error = 0;
    int32_t raw = static_cast<int32_t>(deg * 4096.0 / 360.0);
    packetHandler_->write4ByteTxRx(
      portHandler_,
      id_,
      ADDR_GOAL_POSITION,
      static_cast<uint32_t>(raw),
      &dxl_error
    );
}

DynState DynamixelSDKWrapper::readState() {
  DynState s{};

  // Bulk read
  bulkRead_.txRxPacket();

  auto pos_raw  = bulkRead_.getData(id_, ADDR_PRESENT_POSITION,     4);
  auto curr_raw = bulkRead_.getData(id_, ADDR_PRESENT_CURRENT,      2);
  auto  volt_raw = bulkRead_.getData(id_, ADDR_PRESENT_INPUT_VOLTAGE,1);

  s.pos     = pos_raw  * 360.0 / 4096.0;
  s.current = static_cast<double>(curr_raw);
  s.voltage = volt_raw * 0.1;

  return s;
}