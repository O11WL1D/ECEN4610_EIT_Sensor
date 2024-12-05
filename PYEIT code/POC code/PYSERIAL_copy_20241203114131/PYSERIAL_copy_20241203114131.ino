void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud
}

void loop() {
  if (Serial.available() > 0) { // Check if data is available
    String data = Serial.readStringUntil('\n'); // Read the incoming data
    Serial.print("INCOMING DATA: "); // Optionally, echo the data back
    Serial.println(data);

    Serial.println("-46.60988228");
    Serial.println("-41.99007778");
    Serial.println("-42.94571846");
    Serial.println("-35.48271961");
    

  }
}
