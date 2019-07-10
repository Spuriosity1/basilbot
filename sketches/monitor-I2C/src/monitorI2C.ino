#include <Wire.h>

#define DEBUG

#ifdef DEBUG
#warning "Debug is enabled!"
#endif

#define SOILPWR 11
#define SOILSIG A0

#define MOTORPWR 5
#define MOTORDTEC A1

#define BUFSIZE 16

#define CHANNEL 0x03

int readMoisture(byte power, int dlay){
    analogWrite(SOILPWR,power);
    delay(dlay);
    int moisture = analogRead(A0);
    analogWrite(SOILPWR,0);
    return moisture;
}

void motorPulse(byte power, int dlay){
    // Motor is active low
    analogWrite(MOTORPWR,255-power);
    delay(dlay);
    analogWrite(MOTORPWR,255);
    delay(1000);
}

void setup() {
    // put your setup code here, to run once:
    pinMode(SOILSIG, INPUT);
    pinMode(SOILPWR, OUTPUT);
    pinMode(MOTORPWR, OUTPUT);
    pinMode(MOTORDTEC, INPUT);

    digitalWrite(MOTORPWR, HIGH);
    Wire.onReceive(receiveEvent);
    Wire.onRequest(requestEvent);
    Wire.begin(CHANNEL);
    Serial.begin(9600);
}

// BYTE STRUCTURE:
// ['S'][speed][time_LSB][time_HSB]

void receiveEvent(int nbytes){
    char msg[nbytes];
    for (int i=0;i<nbytes;i++){
        msg[i]=Wire.read();
    }
    char b=msg[0];
    if (nbytes >= 4 && b == 'S'){
        // S for [S]oak
        // look I don't know why it's like this
        byte fast = msg[1];
        int t = msg[2] + (int)msg[3]<<8;

        // Limit watering to 1 minute
        t = t > 0     ? t : 0;
        t = t < 60000 ? t : 60000;

        motorPulse(fast,t);
        #ifdef DEBUG
        Serial.print("Time: ");
        Serial.println(t);
        #endif
    } else {
        #ifdef DEBUG
        Serial.println("FAILED");
        #endif
    }

}

char sendbuf[BUFSIZE];

// BYTE STRUCTURE
// [soil_LSB][soil_MSB][0][0]

void requestEvent(){
    int moisture = readMoisture(255, 200);
    sendbuf[0] = moisture&0x0f;
    sendbuf[1] = moisture&0xf0;
    for (int i=2; i<BUFSIZE;i++){
        sendbuf[i]=0x00;
    }
    Wire.write(moisture);
}

void loop() {
    delay(100);
}
