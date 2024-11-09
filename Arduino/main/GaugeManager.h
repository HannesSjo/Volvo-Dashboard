#ifndef GAUGEMANAGER_H
#define GAUGEMANAGER_H

class GaugeManager {
public:
  GaugeManager(float adjustment, int rpmPwmPin, int pulseDuration, int speedPwmPin, int tempPwmPin, int dutyCycle);
  void updateGauges(float rpm, float speed, float temp);

private:
  void updateRpm(float rpm, long unsigned int currentMicros);
  void updateSpeed(float speed);
  void updateTemp(float temp);
  void setup(); 
  unsigned long getFrequency(int freq);
  float calculateTemp(float temp);

  // RPM
  const float adjustment;
  const int rpmPwmPin;
  const int pulseDuration;
  int previousMicros;

  // Speed
  const int speedPwmPin;
  int frequency;
  // int halfPeriod;

  // Temperature
  const int tempPwmPin;
  int dutyCycle;
};

#endif
