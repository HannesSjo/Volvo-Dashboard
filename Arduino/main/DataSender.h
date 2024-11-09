#ifndef DATASENDER_H
#define DATASENDER_H

#include "Data.h"
#include <Arduino.h>

class DataSender {
public:
    void sendData(Data data);

private:
    void printAsJson(Data data);
    String formatJsonField(const String& key, float value, bool addComma = true);
};

#endif
