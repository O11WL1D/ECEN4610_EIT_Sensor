void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud
}

void loop() {
  if (Serial.available() > 0) { // Check if data is available
    String data = Serial.readStringUntil('\n'); // Read the incoming data
    Serial.print("INCOMING DATA: "); // Optionally, echo the data back
    Serial.println(data);

    Serial.println("-35.89551149");
    Serial.println("-34.82145407");
    Serial.println("-36.75052789");
    Serial.println("-35.40157074");
    

  }
}
