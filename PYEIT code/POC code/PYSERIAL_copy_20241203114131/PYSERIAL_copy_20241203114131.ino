
const int buttonPin = 8;  // Pin where the button is connected
int buttonState = 0;      // Variable to store button state


void setup() {
   pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600); // Initialize serial communication at 9600 baud
}

void loop() {

    buttonState = digitalRead(buttonPin); 
     if (buttonState == LOW){


    Serial.println("-35.89551149");
    Serial.println("-34.82145407");
    Serial.println("-36.75052789");
    Serial.println("-35.40157074");
    
    delay(1000);
     }


  //}
}

