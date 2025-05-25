#include "MeMegaPi.h"

const byte interruptPin = 18;
const byte NE1 = 31;

uint8_t motorSpeed = 100;

long count = 0;

unsigned long time;
unsigned long last_time;

MeMegaPiDCMotor motor1(PORT1B); // Original motor
MeMegaPiDCMotor motor2(PORT2B); // New motor
MeMegaPiDCMotor motor3(PORT3B); // New motor

void setup()
{
    pinMode(interruptPin, INPUT_PULLUP);
    pinMode(NE1, INPUT);
    attachInterrupt(digitalPinToInterrupt(interruptPin), blink, RISING);
    Serial.begin(9600);

    // Optionally run motors here once, but not necessary since loop() runs them
    motor2.run(motorSpeed);
    motor3.run(motorSpeed);
}

void loop()
{
    // Run all motors continuously
    motor1.run(motorSpeed);
    motor2.run(motorSpeed);
    motor3.run(motorSpeed);

    time = millis();
    if (time - last_time > 2000)
    {
        Serial.println(count);
        last_time = time;
    }
}

void blink()
{
    if (digitalRead(NE1) > 0)
        count++;
    else
        count--;
}
