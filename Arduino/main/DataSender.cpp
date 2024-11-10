#include "DataSender.h"
#include <Arduino.h>

#include "Data.h"

void DataSender::sendData(Data data) {
    //TODO logic
    printAsJson(data);
}

void DataSender::printAsJson(Data data, unsigned long currentMicros) {
    //TODO move to constructor (micros)
    const unsigned long printInterval = 500000;

    static unsigned long lastPrintMicros = 0;
    if (currentMillis - lastPrintMillis >= printInterval) {
        lastPrintMillis = currentMillis;

        String jsonData = "{";
        jsonData += this->formatJsonField("RPM", data.rpm);
        jsonData += this->formatJsonField("TPS", data.tps);
        jsonData += this->formatJsonField("MAP", data.map);
        jsonData += this->formatJsonField("AFR", data.lambda);
        jsonData += this->formatJsonField("IAT", data.intakeAirTemp);
        jsonData += this->formatJsonField("V", data.voltage);
        jsonData += this->formatJsonField("CT", data.coolantTemp);
        jsonData += this->formatJsonField("EP", data.ethanolPercent);
        jsonData += this->formatJsonField("EGT", data.exhaustGasTemp);
        jsonData += this->formatJsonField("OP", data.oilPressure);
        jsonData += this->formatJsonField("OT", data.oilTemp);
        jsonData += this->formatJsonField("LT", data.lambdaTarget);
        jsonData += this->formatJsonField("EC", data.errorCount, false); // Last item, no comma
        jsonData += "}";

        Serial.println(jsonData);
    }
}

String DataSender::formatJsonField(const String& key, float value, bool addComma) {
    String field = "\"" + key + "\":" + String(value, 2);
    if (addComma) field += ",";
    return field;
}
