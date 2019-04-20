#define SOILPWR 11
#define SOILSIG A0

#define MOTORPWR 9


void setup()
{
    pinMode(MOTORPWR,OUTPUT);

    Serial.begin(9600);
    while(!Serial){};
}


void motorPulse(byte power, int dlay){
    analogWrite(MOTORPWR,power);
    delay(dlay);
    analogWrite(MOTORPWR,0);
}

void loop()
{
    if (Serial.available()){
        byte b = Serial.read();
        motorPulse(255, 1000);
    }
}
