#include <Arduino.h>

int readMoisture(int power, int dlay);
void motorPulse(byte power, int dlay);
void setup();
void loop();
#line 1 "src/monitor.ino"
#define SOILPWR 11
#define SOILSIG A0

#define MOTORPWR 9

#define BUFSIZE 16

int readMoisture(int power, int dlay){
    analogWrite(SOILPWR,power);
    delay(dlay);
    int moisture = analogRead(A0);
    analogWrite(SOILPWR,0);
    return moisture;
}

void motorPulse(byte power, int dlay){
    analogWrite(MOTORPWR,power);
    delay(dlay);
    analogWrite(MOTORPWR,0);
}

void setup() {
    // put your setup code here, to run once:
    pinMode(SOILSIG, INPUT);
    pinMode(SOILPWR, OUTPUT);
    pinMode(MOTORPWR, OUTPUT);

    digitalWrite(MOTORPWR, LOW);
    Serial.begin(9600);
}

char buffer[BUFSIZE];
int N = 0;
String msg;
byte speed;


void loop() {
    // put your main code here, to run repeatedly:
    int time=0;
    if (Serial.available()){
        byte b = Serial.read();
        byte c;

        N++;
        if (N >= BUFSIZE) N = 0;
        buffer[N] = b;
        if (b == '\n'){
            c = buffer[0];
            if (c == 'X') {
                msg = String(readMoisture(255, 200));
                Serial.println(msg);
            } else if (c == 'S'){
                speed = buffer[1];
                time += buffer[2];
                time += ((int)buffer[3])<<8;
                Serial.print("Time: ");
                Serial.println(time);
                motorPulse(speed,time);
            } else if (c == 'A'){
                Serial.println("Hello");
            } else {
                Serial.println("FAILED");
            }
            N=BUFSIZE;
        }
    }

}
