#ifndef CANHANDLER_H
#define CANHANDLER_H

#include <mcp2515.h>
#include <map>
#include <tuple>

class CANHandler {
public:
    CANHandler(int csPin);
    void initialize();
    void readMessages();
    
    int rpm;
    int tps;
    int map;
    float lambda;
    int intakeAirTemp;
    int voltage;
    int coolantTemp;
    int ethanolPercent;
    int exhaustGasTemp;
    int oilPressure;
    int oilTemp;
    float lambdaTarget;
    int errorCount;

private:
    MCP2515 mcp2515;

    int decodeInt(can_frame msg, int offset, int length, float scale);

    std::map<uint16_t, std::vector<std::tuple<int, int*, float>>> canMap;

    void initializeCanMap();
};

#endif
