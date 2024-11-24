#ifndef GAUGEMANAGER_H
#define GAUGEMANAGER_H

class GaugeManager {
public:
  GaugeManager(float adjustment, int rpmPwmPin, int pulseDuration, int speedPwmPin, int tempPwmPin, int dutyCycle);
  void updateGauges(float rpm, float speed, float temp, unsigned long currentMicros);

private:
  void updateRpm(float rpm, long unsigned int currentMicros);
  void updateSpeed(float speed, unsigned long currentMicros);
  void updateTemp(float temp, unsigned long currentMicros);
  void updateGas(float gas, unsigned long currentMicros);
  void setup(); 
  unsigned long getFrequency(int freq);
  int calculateTemp(float temp);

  // RPM
  const float adjustment;
  const int rpmPwmPin;
  const int pulseDuration;
  long previousMicros;

  // Speed
  const int speedPwmPin;
  int frequency;
  // int halfPeriod;

  // Temperature
  const int tempPwmPin;
  int dutyCycle;

  // Gas
  const int gasPwmPin;
};

#endif
