#include <Wire.h>
#include <util/atomic.h>

#ifdef DEBUG
#warning "Debug is enabled!"
#endif

#define SOILPWR 11
#define SOILSIG A0

#define MOTORPWR 5
#define MOTORDTEC A1

// MUST FIT IN 1 BYTE
#define BUFSIZE 16

#define CHANNEL 0x03

// FSM time
#define IN_STATE 0xF0
#define READY_STATE 0x00


volatile byte state  = READY_STATE;
volatile byte cmd_buffer[BUFSIZE];
volatile byte n_cmd_bytes = 0;
byte out_buffer[BUFSIZE];

//////////////////////////////////////////////////////////////
// ISR FUNCTIONS
// DO NOT RELY ON INTERRUPTS HEREIN

void receiveEvent(int N){
    if (state == READY_STATE){
        n_cmd_bytes = (N < BUFSIZE) ? N : BUFSIZE;
        for (int i = 0; i < N; i++) {
            if (i < BUFSIZE) {
                cmd_buffer[i] = Wire.read();
            } else {
                // Ignore any extra bytes
                Wire.read();
            }
        }
        state = IN_STATE;
    } else {
        for (int i = 0; i < N; i++) {
                // Ignore any extra bytes
                Wire.read();
        }
    }
}

void requestEvent(){
    Wire.write(out_buffer, BUFSIZE);
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

    digitalWrite(MOTORPWR, HIGH);

    Wire.onReceive(receiveEvent);
    Wire.onRequest(requestEvent);
    Wire.begin(CHANNEL);

    #ifdef DEBUG
    Serial.begin(9600);
    #endif
}






// IN BYTE STRUCTURE:
// ['S'][speed][time_LSB][time_HSB]

// OUT BYTE STRUCTURE
// [soil_LSB][soil_MSB][0][0]

void parse(){
    byte static_cmd[BUFSIZE];
    byte nbytes = n_cmd_bytes;
    ATOMIC_BLOCK(ATOMIC_RESTORESTATE){
        for (size_t i = 0; i < BUFSIZE; i++) {
            static_cmd[i] = cmd_buffer[i];
        }
    }
    switch (static_cmd[0]) {
        case 'W':
            // W for [W]ater
            if (nbytes >= 4){
                byte fast = static_cmd[1];
                word t = static_cmd[2] + (word) static_cmd[3] << 8;
                // Limit watering to 1 minute
                t = t < 60000 ? t : 60000;
                motorPulse(fast,t);
            }
            break;
        case 'M':
            // Pre-measurement call
            if (nbytes >= 4){
                byte fast = static_cmd[1];
                word t = static_cmd[2] + (word) static_cmd[3] << 8;
                int val = readMoisture(255,t);
                out_buffer[0] = val & 0xFF;
                out_buffer[1] = val >> 8;
                for (size_t i = 2; i < BUFSIZE; i++) {
                    out_buffer[i] = 0x00;
                }
            }
            break;
    }

}



void loop() {
    if (state == IN_STATE) {
        parse();
        state = READY_STATE;
    }
    // else if (state == OUT_STATE) {
    //     for (int i = 0; i < BUFSIZE; i++) {
    //         Wire.write()
    //     }
    // }
}
