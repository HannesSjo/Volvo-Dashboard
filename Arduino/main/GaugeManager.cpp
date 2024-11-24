#include "GaugeManager.h"
#include <Arduino.h>

bool pulseState = false;


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
  updateGas(90.0, currentMicros);
}

// RPM
void GaugeManager::updateRpm(float rpm, long unsigned int currentMicros) {
  float pulseFrequency = (rpm * this->adjustment) / 60.0;
  float pulseIntervalMicros = 1000000.0 / pulseFrequency;
  int b = pulseState ? this->pulseDuration : pulseIntervalMicros;

  if (currentMicros - this->previousMicros >= b) {
    this->previousMicros = currentMicros;
    if (pulseState) 
      digitalWrite(this->rpmPwmPin, LOW);
    else
      digitalWrite(this->rpmPwmPin, HIGH);
    pulseState = !pulseState;
  }
}

// SPEED
void GaugeManager::updateSpeed(float speed, unsigned long currentMicros) {
  static unsigned long lastToggleMicros = 0;
  static bool speedPinState = false;
  // unsigned long period = 1000000 / freq;
  unsigned long halfPeriod = (1000000 / speed) / 2;
  // unsigned long halfPeriod = this->getFrequency(speed);

  if (currentMicros - lastToggleMicros >= halfPeriod) {
    lastToggleMicros = currentMicros;
    speedPinState = !speedPinState;
    digitalWrite(this->speedPwmPin, speedPinState ? HIGH : LOW);
  }
}

// TEMP
void GaugeManager::updateTemp(float temp, unsigned long currentMicros) {
  static unsigned long lastUpdateMicros = 0;
  
  if (currentMicros - lastUpdateMicros >= 100) {
    lastUpdateMicros = currentMicros;
    float t = this->calculateTemp(temp);
    analogWrite(this->tempPwmPin, t);
  }
}

void GaugeManager::updateGas(float gas, unsigned long currentMicros) {
  static unsigned long lastUpdateMicros = 0;
  
  if (currentMicros - lastUpdateMicros >= 100) {
    lastUpdateMicros = currentMicros;
    float t = this->calculateTemp(gas);
    analogWrite(6, 255);
  }
}

// UTILS
void GaugeManager::setup() {
  pinMode(this->rpmPwmPin, OUTPUT);

  pinMode(this->speedPwmPin, OUTPUT);

  pinMode(this->tempPwmPin, OUTPUT);
}

unsigned long GaugeManager::getFrequency(int freq) {
  
}

int GaugeManager::calculateTemp(float temp) {
  // TODO
  // 25 pwm value = MIN, 70 C
  // 108 pwm value = MID, 90 C
  // 190 pwm value = MAX, 110 C

  float value = 25 + (temp - 70) * (190 - 25) / (110 - 70);

  if (value < 0) value = 0;
  else if (value > 255) value = 255;

  return static_cast<int>(value);
}