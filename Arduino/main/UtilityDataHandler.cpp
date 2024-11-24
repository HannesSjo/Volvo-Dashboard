#include "UtilityDataHandler.h"

UtilityDataHandler::UtilityDataHandler() {
    gpsSerial = &Serial1;
    gpsSerial->begin(9600);
}

float UtilityDataHandler::getGpsSpeed() {
    while (gpsSerial->available() > 0) {
        char c = gpsSerial->read();
        gps.encode(c);
    }

    if (gps.speed.isUpdated()) {
        return gps.speed.kmph();
    }

    return 0.0;
}