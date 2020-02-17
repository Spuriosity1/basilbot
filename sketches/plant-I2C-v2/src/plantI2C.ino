#include <Wire.h>
#include <util/atomic.h>

// Hardware pins
#define SOILPWR 11
#define SOILSIG A0

#define MOTORPWR 5
#define MOTORDTEC A1


#define BUFSIZE 16

#define CHANNEL 0x08




// FSM time
#define IN_STATE 0xFF    // There is an unprocessed command loaded into the buffer
#define READY_STATE 0x00 // Prepared to accept instructions
#define AUTO_STATE 0x01  // Timeout activated, autowater engaged

volatile byte state = READY_STATE;
volatile byte nbytes = 0;
volatile byte buffer[BUFSIZE];
// Index to map particular read register
volatile byte idx = 0;


volatile unsigned long laTime = millis(); // last access time

const unsigned long autoTime = 1000*3600*24; // 1 day
#define AUTO_SECONDS 3600 // Number of seconds bewween autochecks

//////////////////////////////////////////////////////////////
// ISR FUNCTIONS
// DO NOT RELY ON INTERRUPTS HEREIN

void receiveEvent(int N){
    laTime = millis();
    if (state == READY_STATE){
        nbytes = N;
        state = IN_STATE;
    }
}

void requestEvent(){
    laTime = millis();
    Wire.write(buffer[idx]);
}

///////////////////////////////////////////////////////////

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
    pinMode(13, OUTPUT);

    digitalWrite(MOTORPWR, HIGH);

    Wire.begin(CHANNEL);
    Wire.onReceive(receiveEvent);
    Wire.onRequest(requestEvent);

    #ifdef DEBUG
    Serial.begin(9600);
    #endif
}

unsigned int n = 0;
bool LEDstate = false;
void loop() {
    if (state == IN_STATE) {
        switch (Wire.read()) {
            case 'W':
                // W for [W]ater
                if (nbytes >= 4){
                    byte fast = Wire.read();
                    word t = Wire.read();
                    t += (word) Wire.read() << 8;
                    // Limit watering to 1 minute
                    t = t < 60000 ? t : 60000;
                    motorPulse(fast,t);
                }
                break;
            case 'M':
                // Pre-measurement call
                if (nbytes >= 4){
                    byte fast = Wire.read();
                    word t = Wire.read();
                    t += (word) Wire.read() << 8;
                    int val = readMoisture(255,t);
                    buffer[0] = (byte) (val >>2); // MAKE IT FIT IN ONE BYTE
                    // Everything else is fuckin' zero
                    for (size_t i = 1; i < BUFSIZE; i++) {
                        buffer[i] = 0x00;
                    }
                }
                break;
            case 'R':
                // Read call
                if (nbytes >= 2){
                    idx = Wire.read();
                }
        }
        // Flush the buffer
        while (Wire.available()) {
            Wire.read();
        }
        state = READY_STATE;
    } else if (state == AUTO_STATE){
        if (n == AUTO_SECONDS*10){
            n=0;
            int m = readMoisture(255,100)/5;
            #ifdef DEBUG
            Serial.print("[AUTOWATER] -- read percent ");
            Serial.println(m);
            #endif
            if (m <75){
                motorPulse(255,10000);
            }
        }
        n++;
    }
    if ((unsigned long) (millis() - laTime) > autoTime){
        #ifdef DEBUG
        Serial.println("[AUTOWATER] -- automatic watering");
        #endif
        digitalWrite(13, HIGH);
        LEDstate = !LEDstate;
        digitalWrite(13, LEDstate);
    } else {
        digitalWrite(13, LOW);
    }
    delay(100);
}