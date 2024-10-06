#include "CANHandler.h"
#include "GaugeManager.h"
#include "DataSender.h"

CANHandler canHandler(10);
GaugeManager gaugeManager;
DataSender dataSender;

struct can_frame canMsg;
int FPS = 10;

void setup() {
    Serial.begin(115200);
    canHandler.initialize();
}

void loop() {
    if (canHandler.readMessage(&canMsg)) {
        if (canMsg.can_id == 0x520) {
            int rpm = canHandler.decodeInt(canMsg, 1);
            Serial.print("Engine RPM: ");
            Serial.println(rpm);
        }
    }

    gaugeManager.updateGauges();
    dataSender.sendData();

    delay(1000 / FPS);
}
