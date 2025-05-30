#include <Arduino.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial);
  digitalWrite(13, LOW); // Wait for serial connection

}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {

    String data = Serial.readStringUntil('\n');
    
    // Split into components
    int comma1 = data.indexOf(',');
    int comma2 = data.indexOf(',', comma1+1);
    int comma3 = data.indexOf(',', comma2+1);
    int comma4 = data.indexOf(',', comma3+1);
    
    if (comma1 > 0 && comma2 > 0 && comma3 > 0 && comma4 > 0) {
      int action = data.substring(0, comma1).toInt();
      float center_x = data.substring(comma1+1, comma2).toFloat();
      float center_y = data.substring(comma2+1, comma3).toFloat();
      float width = data.substring(comma3+1, comma4).toFloat();
      float height = data.substring(comma4+1).toFloat();

      digitalWrite(13, HIGH);
      delay(1000);
      digitalWrite(13, LOW);
      
      Serial.print("Received: ");
      Serial.print(action);
      Serial.print(center_x, 5);
      Serial.print(", ");
      Serial.print(center_y, 5);
      Serial.print(", ");
      Serial.print(width, 5);
      Serial.print(", ");
      Serial.println(height, 5);

    }



  }
}
