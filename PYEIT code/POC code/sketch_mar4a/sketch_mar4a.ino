
#include <SPI.h>
#include <RH_RF95.h>

// Define pins for RFM95W 1
#define RFM95_CS_1 10      // Chip Select (NSS) pin
#define RFM95_INT_1 3      // Interrupt pin (G0 or DIO0)

// Define pins for RFM95W 2 (WIRE THIS 8, 7, 6!) 
#define RFM95_CS_2 9      // Chip Select (NSS) pin
#define RFM95_INT_2 2      // Interrupt pin (G0 or DIO0)

// Define pins for RFM95W 3 (LoRa 3)
#define RFM95_CS_3 5      // Chip Select (NSS) pin
#define RFM95_INT_3 18     // Interrupt pin (G0 or DIO0)

#define RFM95_CS_4 4
#define RFM95_INT_4 19

#define RFM95_RST 8      // Reset pin


// Set frequency to match the transmitter
#define RF95_FREQ 915.0


// Initialize the LoRa drivers
RH_RF95 rf95_1(RFM95_CS_1, RFM95_INT_1);
RH_RF95 rf95_2(RFM95_CS_2, RFM95_INT_2);
RH_RF95 rf95_3(RFM95_CS_3, RFM95_INT_3);
RH_RF95 rf95_4(RFM95_CS_4, RFM95_INT_4);



float receivedRSSI[10];
float sum = 0;
float n = 0;
int i = 0;




void setup() {
  Serial.begin(9600);
  delay(1000); // Wait for serial monitor to initialize


  // Initialize the RFM95 1 module
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);
  digitalWrite(RFM95_RST, LOW); 
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(50);
  
  


  if (!rf95_1.init()) {
    Serial.println("LoRa 1 module init failed. Check wiring.");
    while (1); // Halt if module is not found
  }

  delay(500);  // Give time before initializing second module

  if (!rf95_2.init()) {
    Serial.println("LoRa 2 module init failed. Check wiring.");
    while (1); // Halt if module is not found
  }


  if (!rf95_3.init()) {
    Serial.println("LoRa 3 module init failed. Check wiring.");
    while (1); // Halt if module is not found
  }


  if (!rf95_4.init()) {
    Serial.println("LoRa 4 module init failed. Check wiring.");
    while (1); // Halt if module is not found
  }



  Serial.println("All LoRa modules initialized successfully.");

  // Set the frequencies
  if (!rf95_2.setFrequency(RF95_FREQ)) {
    Serial.println("Failed to set frequency on LoRa 2.");
    while (1); // Halt if frequency setting fails
  }

  if (!rf95_1.setFrequency(RF95_FREQ)) {
    Serial.println("Failed to set frequency on LoRa 1.");
    while (1); // Halt if frequency setting fails
  }

  if (!rf95_3.setFrequency(RF95_FREQ)) {
    Serial.println("Failed to set frequency on LoRa 3.");
    while (1); // Halt if frequency setting fails
  }


  if (!rf95_4.setFrequency(RF95_FREQ)) {
    Serial.println("Failed to set frequency on LoRa 4.");
    while (1); // Halt if frequency setting fails
  }
  
  Serial.print("Frequency set to ");
  Serial.print(RF95_FREQ);
  Serial.println(" MHz on both LoRa");

  delay(500);
}

void loop(){
  i += 1;

  if (i == 1) {
    rf95_1.setTxPower(20, false);
    rf95_2.setTxPower(20, false);
  }

  Serial.print("---------------");
  Serial.print(i);
  Serial.println("---------------");

  delay(100);

  transmit(rf95_1);
  receivedRSSI[0] = receive(rf95_2);
  receivedRSSI[1] = receive(rf95_4);

  delay(100);

  transmit(rf95_2);
  receivedRSSI[2] = receive(rf95_1);
  receivedRSSI[3] = receive(rf95_3);

  delay(100);

  transmit(rf95_3);
  receivedRSSI[4] = receive(rf95_2);
  receivedRSSI[5] = receive(rf95_4);

  delay(100);


  transmit(rf95_4);
  receivedRSSI[6] = receive(rf95_1);
  receivedRSSI[7] = receive(rf95_3);

  delay(100);



  Serial.print("Array: ");
  Serial.print(receivedRSSI[0]);
  Serial.print(", ");
  Serial.print(receivedRSSI[1]);
  Serial.print(", ");
  Serial.print(receivedRSSI[2]);
  Serial.print(", ");
  Serial.print(receivedRSSI[3]);
  Serial.print(", ");
  Serial.print(receivedRSSI[4]);
  Serial.print(", ");
  Serial.print(receivedRSSI[5]);
  Serial.print(", ");
  Serial.print(receivedRSSI[6]);
  Serial.print(", ");
  Serial.println(receivedRSSI[7]);


  if(i >= 10) {
    while(true) {}
  }
  
}


void transmit(RH_RF95 &transmitLoRa) {
  
  // rf95.setTxPower(20, false);
  
  const char *message = "H"; // The message to transmit
 
  
  Serial.print("Sending: ");
  Serial.println(message);
  transmitLoRa.send((uint8_t *)message, strlen(message));
  

}




int receive(RH_RF95 &receiveLoRa) {

  //receiveLoRa.setTxPower(6, false);
  // Check if a message is available
 
  if (receiveLoRa.available()) {
    
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN]; // Buffer for the received message
    uint8_t len = sizeof(buf);

    // Receive the message
    if (receiveLoRa.recv(buf, &len)) {
     
      if(receiveLoRa.lastRssi()<0){
      n++;
      sum+=receiveLoRa.lastRssi();
      }
      if(n == 100){
        Serial.print("Final average:");
      }
      Serial.print(n);
      Serial.print(", ");
      Serial.println(receiveLoRa.lastRssi());
      return receiveLoRa.lastRssi();

    } else {
      Serial.println("Receive failed");
      return 0;
    }
  }
  else{
    Serial.println("No Message Available...");
    return 0;
  }
}
