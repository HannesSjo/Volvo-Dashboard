#ifndef DATASENDER_H
#define DATASENDER_H

#include "Data.h"
#include <Arduino.h>

class DataSender {
public:
    void sendData(Data data, unsigned long currentMicros);

private:
    void printAsJson(Data data, unsigned long currentMicros);
    String formatJsonField(const String& key, float value, bool addComma = true);
};

#endif
