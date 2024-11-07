#include <Arduino.h>

// put function declarations here:
int myFunction(int, int);
const int ledPin = 13;

void setup() {
  // put your setup code here, to run once:
  int result = myFunction(2, 3);
   pinMode(ledPin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
   digitalWrite(ledPin, HIGH);  // Turn the LED on
  delay(1000);                 // Wait for one second
  digitalWrite(ledPin, LOW);   // Turn the LED off
  delay(1000);    
}

// put function definitions here:
int myFunction(int x, int y) {
  return x + y;
}