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
  for (int angle = 0; angle <= 180; angle += 5) {
    servo1.write(angle); // Move servo1 to specified angle
    delay(100);
  }

  for (int angle = 180; angle >= 0; angle -= 5) {
    servo2.write(angle); // Move servo2 to specified angle
    delay(100);
  }

  delay(1000); // Pause for 1 second

  for (int angle = 0; angle <= 180; angle += 10) {
    servo1.write(angle); // Move servo1 to specified angle
    delay(200);
  }

  for (int angle = 180; angle >= 0; angle -= 10) {
    servo2.write(angle); // Move servo2 to specified angle
    delay(200);
  }

  delay(1000); // Pause for 1 second

  for (int angle = 0; angle <= 180; angle += 20) {
    servo1.write(angle); // Move servo1 to specified angle
    delay(300);
  }

  for (int angle = 180; angle >= 0; angle -= 20) {
    servo2.write(angle); // Move servo2 to specified angle
    delay(300);
  }

  delay(1000); // Pause for 1 second

  for (int angle = 0; angle <= 180; angle += 30) {
    servo1.write(angle); // Move servo1 to specified angle
    delay(400);
  }

  for (int angle = 180; angle >= 0; angle -= 30) {
    servo2.write(angle); // Move servo2 to specified angle
    delay(400);
  }

  delay(1000); // Pause for 1 second
}
