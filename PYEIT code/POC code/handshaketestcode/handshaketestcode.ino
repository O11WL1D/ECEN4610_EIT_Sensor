void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);


}

void loop() {
  // put your main code here, to run repeatedly:



   String data = Serial.readStringUntil('\n'); 

    Serial.print("ARD:");
    Serial.println(data); // Echo it back

  String data1=String(data);


  if(data1=="2"){
      Serial.println("ARD:TESTING!");

  
  Serial.println("ARD:TESTING2!");

  
  Serial.println("ARD:TESTING3!");


  delay(1000);


  Serial.println("1");
    Serial.println("10");
     Serial.println("12");
      Serial.println("12");
       Serial.println("12");





  }

   




}


