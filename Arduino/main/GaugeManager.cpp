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

void GaugeManager::updateGauges(float rpm, float speed, float temp) {
  updateRpm(rpm, micros());
  updateSpeed(speed);
  updateTemp(temp);
}

// RPM
void GaugeManager::updateRpm(float rpm, long unsigned int currentMicros) {
  float pulseFrequency = (rpm * this->adjustment) / 60.0;
  float pulseIntervalMicros = 1000000.0 / pulseFrequency;

  if (currentMicros - previousMicros >= pulseIntervalMicros) {
    previousMicros = currentMicros;

    analogWrite(this->rpmPwmPin, 255);
    delayMicroseconds(this->pulseDuration);
    analogWrite(this->rpmPwmPin, 0);
  }
}

// SPEED
void GaugeManager::updateSpeed(float speed) {
  unsigned long halfPeriod = this->getFrequency(speed);

  digitalWrite(this->speedPwmPin, HIGH);
  delayMicroseconds(halfPeriod);
  
  digitalWrite(this->speedPwmPin, LOW);
  delayMicroseconds(halfPeriod);
}

// TEMP
void GaugeManager::updateTemp(float temp) {
  // TODO
  float t = this->calculateTemp(temp);
  // Serial.println(t);
  int pwmValue = map(this->dutyCycle, 0, 100, 0, 255);
  analogWrite(this->tempPwmPin, pwmValue);

  //dutyCycle--;
  //if (dutyCycle <= 0) dutyCycle = 46;

  delay(100);
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