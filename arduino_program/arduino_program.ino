#include "MeMegaPi.h"

const byte interruptPin = 18;
const byte NE1 = 31;

uint8_t motorSpeed = 200;  // increase motor speed

long count = 0;

unsigned long time;
unsigned long last_time;

// Define 4 motor objects
MeMegaPiDCMotor motor1(PORT1B);
MeMegaPiDCMotor motor2(PORT2B);
MeMegaPiDCMotor motor3(PORT3B);
MeMegaPiDCMotor motor4(PORT4B);

void setup()
{
    pinMode(interruptPin, INPUT_PULLUP);
    pinMode(NE1, INPUT);
    attachInterrupt(digitalPinToInterrupt(interruptPin), blink, RISING);
    Serial.begin(9600);   

    // (Optional) small delay to allow serial to connect
    delay(2000);
}

void loop()
{
    // Run all 4 motors
    motor1.run(motorSpeed);
    motor2.run(motorSpeed);
    motor3.run(motorSpeed);
    motor4.run(motorSpeed);

    time = millis(); 
    if (time - last_time > 2000)
    {
        Serial.print("Count: ");
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
