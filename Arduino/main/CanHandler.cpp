#include "CanHandler.h"
#include <Arduino.h>
#include "Data.h"

bool DEBUG = true;

CANHandler::CANHandler(int csPin) : mcp2515(csPin) {
  initializeCanMap();
}

void CANHandler::initialize() {
    mcp2515.reset();
    mcp2515.setBitrate(CAN_500KBPS, MCP_8MHZ);
    mcp2515.setNormalMode();
}

void CANHandler::initializeCanMap() {
    canMap[numMappings++] = {0x520, 0, &Data::rpm, 1.0f};      // RPM
    canMap[numMappings++] = {0x520, 2, &Data::tps, 0.1f};      // TPS
    canMap[numMappings++] = {0x520, 4, &Data::map, 0.1f};      // MAP
    canMap[numMappings++] = {0x520, 6, &Data::lambda, 0.001f}; // Lambda/AFR

    canMap[numMappings++] = {0x524, 2, &Data::lambdaTarget, 0.001f}; // Lambda Target

    canMap[numMappings++] = {0x530, 0, &Data::voltage, 0.01f};   // Voltage
    canMap[numMappings++] = {0x530, 4, &Data::intakeAirTemp, 0.1f}; // Intake Air Temp
    canMap[numMappings++] = {0x530, 6, &Data::coolantTemp, 0.1f};   // Coolant Temp

    canMap[numMappings++] = {0x531, 2, &Data::ethanolPercent, 0.1f}; // Ethanol Percent
    canMap[numMappings++] = {0x531, 6, &Data::exhaustGasTemp, 1.0f}; // Exhaust Gas Temp

    canMap[numMappings++] = {0x536, 4, &Data::oilPressure, 0.1f};    // Oil Pressure
    canMap[numMappings++] = {0x536, 6, &Data::oilTemp, 0.1f};        // Oil Temp

    canMap[numMappings++] = {0x534, 4, &Data::errorCount, 1.0f};     // Error Count
}

void CANHandler::readMessage() {
    struct can_frame canMsg;
    if(DEBUG) {
      data.*(canMap[0].variable) += 1;
      data.*(canMap[1].variable) += 1;
      data.*(canMap[2].variable) += 0.01;
      data.*(canMap[3].variable) += 0.01;
      data.*(canMap[4].variable) += 1;
      data.*(canMap[5].variable) += 0.1;
      data.*(canMap[6].variable) += 1;
      data.*(canMap[7].variable) += 0.1;
      data.*(canMap[8].variable) += 1;
      data.*(canMap[9].variable) += 0.1;
      data.*(canMap[10].variable) += 1;
      data.*(canMap[11].variable) += 0.1;
      data.*(canMap[12].variable) += 1;
      return;
    }
    if (mcp2515.readMessage(&canMsg) == MCP2515::ERROR_OK) {
        uint16_t canId = canMsg.can_id;

        for (int i = 0; i < numMappings; i++) {
            if (canMap[i].canId == canId) {
                float value = decodeFloat(canMsg, canMap[i].offset, 2, canMap[i].scale);
                data.*(canMap[i].variable) = value;
            }
        }
    }
}

float CANHandler::decodeFloat(can_frame msg, int offset, int length, float scale) {
    int16_t result = 0;
    for (int i = 0; i < length; i++) {
        result |= msg.data[offset + i] << (8 * i);
    }
    return result * scale;
}

const Data& CANHandler::getData() const {
  return data;
}
