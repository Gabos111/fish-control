#pragma once
#include <string>
#include <dynamixel_sdk/dynamixel_sdk.h>
#include <dynamixel_sdk/group_bulk_read.h>
#include <cstdint>

// Simple POD to hold one read‐cycle of position / current / voltage
struct DynState {
    double pos;      // degrees
    double current;  // mA
    double voltage;  // V
};

class DynamixelSDKWrapper {
public:
    // ctor: opens port + protocol handler
    DynamixelSDKWrapper(const std::string& port, int baud, uint8_t id);

    // send a goal position in degrees
    void setPositionDeg(double deg);

    // read back the present state
    DynState readState();

private:
    dynamixel::PortHandler*   portHandler_;
    dynamixel::PacketHandler* packetHandler_;
    uint8_t                  id_;
    // Bulk-reader
    dynamixel::GroupBulkRead bulkRead_;
};