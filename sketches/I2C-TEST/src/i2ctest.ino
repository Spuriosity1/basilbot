#include <Wire.h>

#define SLAVE_ADDRESS 0x08

byte b[4] = {99, 223, 244};
// data buffer
int data[9];

void receiveData(int byteCount){
  int counter = 0;
  while(Wire.available()) {
      data[counter] = Wire.read();
      Serial.print("Got data: ");
      Serial.println(data[counter]);
      counter ++;
  }
}

void sendData(){
    Wire.write(b, 4);
    Serial.println("data sent");
}

void setup(){
  Serial.begin(9600); // start serial for output
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  Serial.println("I2C Ready!");
}

void loop(){
  delay(1000);
}
