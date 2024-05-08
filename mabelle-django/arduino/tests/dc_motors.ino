#include <Arduino.h>

// Motor pins
const int enA = 10;
const int enB = 11;
const int in1 = A0;
const int in2 = A1;
const int in3 = A2;
const int in4 = A3;

// Motor speeds
const int motorSpeed = 255; // Maximum speed

void setup() {
  // Initialize motor pins
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  // Set motor speeds to 0 initially
  analogWrite(enA, 0);
  analogWrite(enB, 0);
}

void loop() {
  // Test forward motion
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enA, motorSpeed);
  analogWrite(enB, motorSpeed);
  delay(2000); // Run forward for 2 seconds

  // Test backward motion
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  delay(1000); // Reverse direction for 1 second

  // Test turning left
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  delay(1000); // Turn left for 1 second

  // Test turning right
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  delay(1000); // Turn right for 1 second

  // Stop motors
  analogWrite(enA, 0);
  analogWrite(enB, 0);
  delay(1000); // Pause for 1 second before next test
}
