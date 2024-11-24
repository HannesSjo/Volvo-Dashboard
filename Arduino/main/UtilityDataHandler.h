#ifndef UTILITYDATAHANDLER_H
#define UTILITYDATAHANDLER_H

#include <TinyGPS++.h>

class UtilityDataHandler {
    public:
        UtilityDataHandler();
        float getGpsSpeed();
    private:
        TinyGPSPlus gps;
        HardwareSerial* gpsSerial;
};

#endif