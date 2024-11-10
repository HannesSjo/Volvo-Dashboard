#include "GaugeManager.h"
#include <Arduino.h>

GaugeManager::GaugeManager(
  float adjustment, int rpmPwmPin, int pulseDuration, 
  int speedPwmPin,
  int tempPwmPin, int dutyCycle
) 
: adjustment(adjustment), rpmPwmPin(rpmPwmPin), pulseDuration(pulseDuration), previousMicros(0),
  speedPwmPin(speedPwmPin),
  tempPwmPin(tempPwmPin), dutyCycle(dutyCycle)
{
  this->setup();
}

void GaugeManager::updateGauges(float rpm, float speed, float temp, unsigned long currentMicros) {
  updateRpm(rpm, currentMicros);
  updateSpeed(speed, currentMicros);
  updateTemp(temp, currentMicros);
}

// RPM
void GaugeManager::updateRpm(float rpm, long unsigned int currentMicros) {
  float pulseFrequency = (rpm * this->adjustment) / 60.0;
  float pulseIntervalMicros = 1000000.0 / pulseFrequency;

  bool pulseState = false;

  if (currentMicros - previousMicros >= pulseState ? this->pulseDuration : pulseIntervalMicros) {
    previousMicros = currentMicros;

    if (pulseState) 
      analogWrite(this->rpmPwmPin, 0);
    else
      analogWrite(this->rpmPwmPin, 255);
    pulseState = !pulseState;
  }
}

// SPEED
void GaugeManager::updateSpeed(float speed, unsigned long currentMicros) {
  static unsigned long lastToggleMicros = 0;
  unsigned long halfPeriod = this->getFrequency(speed);
  static bool speedPinState = false;

  if (currentMicros - lastToggleMicros >= halfPeriod) {
    lastToggleMicros = currentMicros;
    speedPinState = !speedPinState;
    digitalWrite(this->speedPwmPin, speedPinState ? HIGH : LOW);
  }
}

// TEMP
void GaugeManager::updateTemp(float temp, unsigned long currentMillis) {
  static unsigned long lastUpdateMillis = 0;

  if (currentMillis - lastUpdateMillis >= 100) {
    lastUpdateMillis = currentMillis;
    float t = this->calculateTemp(temp);
    int pwmValue = map(this->dutyCycle, 0, 100, 0, 255);
    analogWrite(this->tempPwmPin, pwmValue);

    // Uncomment if you want to modify dutyCycle periodically
    // dutyCycle--;
    // if (dutyCycle <= 0) dutyCycle = 46;
  }
}

// UTILS
void GaugeManager::setup() {
  pinMode(this->rpmPwmPin, OUTPUT);

  pinMode(this->speedPwmPin, OUTPUT);
  // this->setFrequency(frequency);

  pinMode(this->tempPwmPin, OUTPUT);
}

unsigned long GaugeManager::getFrequency(int freq) {
  unsigned long period = 1000000 / freq;
  // this->halfPeriod = period / 2;
  return period / 2;
}

float GaugeManager::calculateTemp(float temp) {
  // TODO
  return temp;
}