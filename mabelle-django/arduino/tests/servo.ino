#include <Servo.h>

// Servo motor pins
const int servoPin1 = 9;
const int servoPin2 = 10;

Servo servo1;
Servo servo2;

void setup() {
  // Attach servo motors to pins
  servo1.attach(servoPin1);
  servo2.attach(servoPin2);
}

void loop() {
  // Test servo movement
  testServo(servo1, 5, 100);
  testServo(servo2, -5, 100);
  delay(1000); // Pause for 1 second

  testServo(servo1, 10, 200);
  testServo(servo2, -10, 200);
  delay(1000); // Pause for 1 second

  testServo(servo1, 20, 300);
  testServo(servo2, -20, 300);
  delay(1000); // Pause for 1 second

  testServo(servo1, 30, 400);
  testServo(servo2, -30, 400);
  delay(1000); // Pause for 1 second
}

void testServo(Servo servo, int stepSize, int delayTime) {
  for (int angle = 0; angle <= 180; angle += stepSize) {
    servo.write(angle); // Move servo to specified angle
    delay(delayTime);
  }
}