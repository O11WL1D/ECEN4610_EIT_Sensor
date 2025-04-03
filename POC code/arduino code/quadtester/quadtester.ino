
//Wavegen Warriors
//Updated: April 2nd, 2025
//Peter Braza, Ahmed Khan, Gavin Unrue, Dante Ausonio, Graham Snyder, Gustavo Sanchez Sanchez

//Header files and .cpp files from Radiohead Library has been manually changed to allow for 6 LoRa
#include <SPI.h>
#include <RH_RF95.h>

// Define pins for RFM95W 1
#define RFM95_CS_1 4      // Chip Select (NSS) pin
#define RFM95_INT_1 2     // Interrupt pin (G0 or DIO0)

// Define pins for RFM95W 2 
#define RFM95_CS_2 6      // Chip Select (NSS) pin
#define RFM95_INT_2 3     // Interrupt pin (G0 or DIO0)

// Define pins for RFM95W 3 
#define RFM95_CS_3 9      // Chip Select (NSS) pin
#define RFM95_INT_3 18    // Interrupt pin (G0 or DIO0)

// Define pins for RFM95W 4 
#define RFM95_CS_4 10     // Chip Select (NSS) pin
#define RFM95_INT_4 19    // Interrupt pin (G0 or DIO0)

#define RFM95_RST 8       // Reset pin

// Set frequency to 915 MHz as specified by LoRa
#define RF95_FREQ 915.0

// Initialize the LoRa drivers: Chip select and interrupt assigned to each new LoRa variable
RH_RF95 rf95_1(RFM95_CS_1, RFM95_INT_1);
RH_RF95 rf95_2(RFM95_CS_2, RFM95_INT_2);
RH_RF95 rf95_3(RFM95_CS_3, RFM95_INT_3);
RH_RF95 rf95_4(RFM95_CS_4, RFM95_INT_4);



void setup() {
  Serial.begin(9600); 
  delay(1000); // Wait for serial monitor to initialize
  
  // Initialize the RFM95 Reset module
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);
  digitalWrite(RFM95_RST, LOW); 
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(50);
  

  //Initialize each of the four sensors. If wiring is incorrect, will say the initialization failed.
  if (!rf95_1.init()) {
    Serial.println("LoRa 1 module init failed. Check wiring.");
    while (1); // Halt if module is not found
  }
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


  // Set the frequencies to defined 915 MHz value
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
  Serial.println(" MHz on all four LoRa sensors");

  delay(500);
}




void loop(){

  int receivedRSSI[4]; //Collects the dBm data from each of the four LoRa sensors
 
  delay(4000);

  //Sensor 4 transmits to sensor 1
  transmit(rf95_4);
  receivedRSSI[0] = receive(rf95_1);
  delay(100);

  //Sensor 1 transmits to sensor 2
  transmit(rf95_1);
  receivedRSSI[1] = receive(rf95_2);
  delay(100);

  //Sensor 2 transmits to sensor 3
  transmit(rf95_2);
  receivedRSSI[2] = receive(rf95_3);
  delay(100);

  //Sensor 3 transmits to sensor 4
  transmit(rf95_3);
  receivedRSSI[3] = receive(rf95_4);
  delay(100); 


  //Print the four collected data values
  Serial.print("\n");
  Serial.print(receivedRSSI[0]);
  Serial.print("\n");
  Serial.print(receivedRSSI[1]);
  Serial.print("\n");
  Serial.print(receivedRSSI[2]);
  Serial.print("\n");
  Serial.print(receivedRSSI[3]);
  Serial.print("\n");

  //Print the quadrant location of the object
  printQuadrant(receivedRSSI);
}


void transmit(RH_RF95 &transmitLoRa) {
  
  //transmitLoRa.setTxPower(20, false);
  const char *message = "H"; // The message to transmit
  transmitLoRa.send((uint8_t *)message, strlen(message));
}




int receive(RH_RF95 &receiveLoRa) {

  receiveLoRa.setTxPower(6, false);
  
  if (receiveLoRa.available()) {    // Check if a message is available
    
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN]; // Buffer for the received message
    uint8_t len = sizeof(buf);

    // Receive the message
    if (receiveLoRa.recv(buf, &len)) { 
      return receiveLoRa.lastRssi(); //successfully received the data
    } 
    else {
      Serial.println("Receive failed");
      return 0;
    }
  }
  else{
    return 0; //No message available
  }
}




void printQuadrant(int sensorData[4]) {
  // Reference arrays for each quadrant
  int NW[4] = {-19, -4, -13, -11};
  int NE[4] = {-13, -9, -16, -2};
  int sE[4] = {-16, -13, -11, -3};
  int SW[4] = {-15, -4, -16, -12};

  // Calculate total difference (error) for each quadrant
  int diffNW = 0;
  int diffNE = 0;
  int diffsE = 0;
  int diffSW = 0;

  for (int i = 0; i < 4; i++) {
    diffNW += abs(sensorData[i] - NW[i]);
    diffNE += abs(sensorData[i] - NE[i]);
    diffsE += abs(sensorData[i] - sE[i]);
    diffSW += abs(sensorData[i] - SW[i]);
  }

  // Determine the quadrant with the smallest error
  int minDiff = diffNW;
  String quadrant = "NW";

  if (diffNE < minDiff) {
    minDiff = diffNE;
    quadrant = "NE";
  }
  if (diffsE < minDiff) {
    minDiff = diffsE;
    quadrant = "SE";
  }
  if (diffSW < minDiff) {
    minDiff = diffSW;
    quadrant = "SW";
  }

  // Print the detected quadrant
  Serial.print("Detected Quadrant: ");
  Serial.println(quadrant);
}