#include "CANHandler.h"
#include <Arduino.h>

CANHandler::CANHandler(int csPin) : mcp2515(csPin) {
    rpm = tps = map = intakeAirTemp = voltage = coolantTemp = ethanolPercent = exhaustGasTemp = oilPressure = oilTemp = errorCount = 0;
    lambda = lambdaTarget = 0.0f;

    initializeCanMap();
}

void CANHandler::initialize() {
    mcp2515.reset();
    mcp2515.setBitrate(CAN_500KBPS, MCP_8MHZ);
    mcp2515.setNormalMode();
    Serial.println("MCP2515 Initialized. Listening for CAN messages...");
}

void CANHandler::initializeCanMap() {
    canMap[0x520] = {
        {0, (int)&rpm, 1.0f},      // RPM
        {2, (int)&tps, 0.1f},      // TPS
        {4, (int)&map, 0.1f},      // MAP
        {6, (int)&lambda, 0.001f} // Lambda/AFR
    };
    canMap[0x521] = {
        {4, (int)&intakeAirTemp, 0.1f} // Intake Air Temp (IA)
    };
    canMap[0x524] = {
        {2, (int)&lambdaTarget, 0.001f} // Lambda Target
    };
    canMap[0x530] = {
        {0, (int)&voltage, 0.01f},      // Voltage
        {4, (int)&intakeAirTemp, 0.1f},// IAT
        {6, (int)&coolantTemp, 0.1f}   // Coolant Temp (CT)
    };
    canMap[0x531] = {
        {2, (int)&ethanolPercent, 0.1f}, // Ethanol %
        {6, (int)&exhaustGasTemp, 1f}  // Exhaust Gas Temp (EGT)
    };
    canMap[0x536] = {
        {4, (int)&oilPressure, 0.1f}, // Oil Pressure
        {6, (int)&oilTemp, 0.1f}      // Oil Temp
    };
    canMap[0x534] = {
        {4, (int)&errorCount, 1f}   // Error count
    };
}

void CANHandler::readMessages() {
    struct can_frame canMsg;

    if (mcp2515.readMessage(&canMsg) == MCP2515::ERROR_OK) {
        uint16_t canId = canMsg.can_id;

        if (canMap.find(canId) != canMap.end()) {
            for (auto &entry : canMap[canId]) {
                int offset = entry.first;
                int* variable = (int*)entry.second;
                *variable = decodeInt(canMsg, offset, 2, 1); // Decode a 2-byte integer with no scaling
            }
        }
    }
}

int CANHandler::decodeInt(can_frame msg, int offset, int length, int scale) {
    int16_t result = 0;

    for (int i = 0; i < length; i++) {
        result |= msg.data[offset + i] << (8 * i);
    }

    return result * scale;
}
