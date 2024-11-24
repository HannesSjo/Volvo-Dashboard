#include "CanHandler.h"
#include "GaugeManager.h"
#include "UtilityDataHandler.h"
#include "DataSender.h"
#include "Data.h"

// RPM Gauge
float rpmAdjustment = 2;
const int rpmPwmPin = 5;
const int rpmPulseDuration = 1500;

// Speed gauge
const int speedPwmPin = 2;

// Temp gauge
const int tempPwmPin = 3;
const int dutyCycle = 10;

CANHandler canHandler(10);
GaugeManager gaugeManager(
  rpmAdjustment, rpmPwmPin, rpmPulseDuration,             // Rpm vars
  speedPwmPin,                                            // Speed vars
  tempPwmPin, dutyCycle                                   // Temp vars
);
DataSender dataSender;
UtilityDataHandler utilHandler;

struct can_frame canMsg;
int RPS = 5;

void setup() {
    Serial.begin(115200);
    canHandler.initialize();
}

void loop() {
    unsigned long currentMicros = micros();
    canHandler.readMessage();
    //TODO read utility data ex speed
    float speed = utilHandler.getGpsSpeed();
    // Serial.println(speed);
    Data data = canHandler.getData();
    gaugeManager.updateGauges(data.rpm, speed + 10.0, data.coolantTemp, currentMicros);
    dataSender.sendData(data, currentMicros);

    // delayMicroseconds(20);
}
