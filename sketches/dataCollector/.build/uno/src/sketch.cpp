#include <Arduino.h>

void setup();
void loop();
#line 1 "src/sketch.ino"
#define LDR1 A1
#define LDR2 A2
#define SOIL A0

#define SOILPWR 5

#define LINEND '\n'

int navg= 64;
int wait= 200;

void setup()
{
	pinMode(LDR1, INPUT);
	pinMode(LDR2, INPUT);
	pinMode(SOIL, INPUT);
	pinMode(SOILPWR, OUTPUT);
	Serial.begin(9600);
	while(!Serial); // Not sure what this does
	digitalWrite(SOILPWR,LOW);
}



void loop()
{
	if (Serial.available()) {
		byte b = Serial.read();

		if (b=='R'){
			digitalWrite(SOILPWR, HIGH);
			delay(300);
			long soil=0;
			long l1=0;
			long l2=0;
		
			for (int i=0; i<navg; i++){
				soil += analogRead(SOIL);
				l1 += analogRead(LDR1);
				l2 += analogRead(LDR2);
				delay(wait);
			}
			Serial.write( (short) soil/navg);
			Serial.write( (short) l1/navg );
			Serial.write( (short) l2/navg );
			
			Serial.write(LINEND);
		}
		
	}
			
}
