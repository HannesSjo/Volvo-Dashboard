#include "CANHandler.h"
#include "GaugeManager.h"
#include "DataSender.h"
#include "Data.h"

CANHandler canHandler(10);
GaugeManager gaugeManager;
DataSender dataSender;

struct can_frame canMsg;
int RPS = 10;

void setup() {
    Serial.begin(115200);
    canHandler.initialize();
}

void loop() {
    canHandler.readMessage();
    //TODO read utility data ex speed
    Data data = canHandler.getData();
    gaugeManager.updateGauges(); //TODO
    dataSender.sendData(data); //TODO

    delay(1000 / RPS);
}
