
const int buttonPin = 8;  // Pin where the button is connected
int buttonState = 0;      // Variable to store button state


void setup() {
   pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600); // Initialize serial communication at 9600 baud
}

void loop() {

    buttonState = digitalRead(buttonPin); 

    Serial.println("SAMPLE TEST");
    Serial.println("SAMPLE TEST");
    Serial.println("ERROR MESSAGE");



     if (buttonState == LOW){


    Serial.println("1");
 
    Serial.println("-10.89551149");
    Serial.println("-10.82145407");
    Serial.println("-10.75052789");
    Serial.println("-10.40157074");

    Serial.println("MORE STUFF");
    Serial.println("asdasdasd");
    Serial.println("TESTING");




    
    delay(1000);
     }


  //}
}

