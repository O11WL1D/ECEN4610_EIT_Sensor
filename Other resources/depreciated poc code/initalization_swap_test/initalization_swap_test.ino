#include <avr/wdt.h>

void setup() {
    Serial.begin(9600);
    Serial.println("Arduino will reset in 3 seconds...");
    delay(3000);
    
    wdt_enable(WDTO_15MS);  // Enable watchdog timer (resets in 15ms)
    while (1);  // Enter an infinite loop to trigger reset
}

void loop() {
    Serial.println("This will never be reached.");
    delay(1000);
}
