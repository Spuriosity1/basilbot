#include <Wire.h>


#ifdef DEBUG
#warning "Debug is enabled!"
#endif

#define SOILPWR 11
#define SOILSIG A0

#define MOTORPWR 5
#define MOTORDTEC A1

#define BUFSIZE 16

#define CHANNEL 0x03

int readMoisture(byte power, word dlay){
    analogWrite(SOILPWR,power);
    delay(dlay);
    int moisture = analogRead(A0);
    analogWrite(SOILPWR,0);
    return moisture;
}

void motorPulse(byte power, word dlay){
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
    #ifdef DEBUG
    Serial.begin(9600);
    #endif
}

// BYTE STRUCTURE:
// ['S'][speed][time_LSB][time_HSB]

void receiveEvent(int nbytes){
    byte msg[nbytes];
    for (int i=0;i<nbytes;i++){
        msg[i]=Wire.read();
    }

    #ifdef DEBUG
    Serial.print("Message:");
    for (int i=0;i<nbytes;i++){
        Serial.print(msg[i]);
        Serial.print('\n');
    }
    Serial.println();
    #endif

    byte b=msg[0];
    if (nbytes >= 4 && b == 'S'){
        // S for [S]oak
        // look I don't know why it's like this
        byte fast = msg[1];
        word t = msg[2] + (word) msg[3] << 8;

        #ifdef DEBUG
        Serial.print("Time: ");
        Serial.println(t);
        #endif

        // Limit watering to 1 minute
        t = t < 60000 ? t : 60000;

        motorPulse(fast,t);

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
