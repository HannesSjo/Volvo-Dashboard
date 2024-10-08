#ifndef CANHANDLER_H
#define CANHANDLER_H

#include <mcp2515.h>
#include "Data.h"

class CANHandler {
public:
    CANHandler(int csPin);
    void initialize();
    void readMessage();
    
    const Data& getData() const;

private:
    MCP2515 mcp2515;
    Data data;

    struct CanMap {
        uint16_t canId;
        int offset;
        float Data::* variable;
        float scale;
    };

    static const int maxMappings = 20;
    CanMap canMap[maxMappings];
    int numMappings = 0;

    float decodeFloat(can_frame msg, int offset, int length, float scale);
    void initializeCanMap();
};

#endif
