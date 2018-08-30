#include "I2Cdev.h"
#include "MPU6050.h"
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include "Wire.h"
#endif

// #define Pin_Inter 23
#define Pin_Led_Control 13
#define Pin_signal_Control 20

#define fin '>'                 // Character separator used for split data

MPU6050 accel;

int16_t ax = 0, ay = 0, az = 0;

bool capture = false, loops = true;

int pint = 0;

bool uno = true, dos = false; 

unsigned long time_count = 0;


void setup() {
  // join I2C bus (I2Cdev library doesn't do this automatically)
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    Wire.begin();
  #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
    Fastwire::setup(400, true);
  #endif

  // Initialize parameters for Stim-Accel communication
  Serial.begin(2000000);
  Serial1.begin(2000000);

  accel.initialize();
  
  //pinMode(Pin_Inter, INPUT);
  pinMode(Pin_signal_Control, INPUT_PULLUP);
  pinMode(Pin_Led_Control, OUTPUT);

  //attachInterrupt(Pin_Inter, Communication_data, CHANGE);
  
  digitalWrite(Pin_Led_Control,1);
}

void loop() {

  time_count = micros() + 5e5;

  led_blink_and_read();

  pint = 0;
  ax = 0;
  ay = 0;
  az = 0;

  if(capture){

    Serial.print(micros());
    Serial.print(";");
    pint = digitalRead(Pin_signal_Control);
    accel.getAcceleration(&ax, &ay, &az);
    Serial.print(ax);
    Serial.print(";");
    Serial.print(ay);
    Serial.print(";");
    Serial.print(az);
    Serial.print(";");
    Serial.println(pint);

    while(capture) {
      pint = digitalRead(Pin_signal_Control);
      //Serial.print(micros());
      Serial.print("0;");
      accel.getAcceleration(&ax, &ay, &az);
      Serial.print(ax);
      Serial.print(";");
      Serial.print(ay);
      Serial.print(";");
      Serial.print(az);
      Serial.print(";");
      Serial.println(pint);
      read_data();      
    } 

    Serial.print(micros());
    Serial.print(";");
    Serial.print(ax);
    Serial.print(";");
    Serial.print(ay);
    Serial.print(";");
    Serial.print(az);
    Serial.print(";");
    Serial.println(pint);
    Serial.println(">");

  }
}

void read_data(){
	if(Serial1.available() != 0){
  		String data_in = Serial1.readStringUntil(fin);
    	int sel1 = data_in.toInt();
    	data_in = Serial1.readStringUntil(fin);
    	int sel2 = data_in.toInt();
    	Serial1.readString();

    	switch (sel1) {
      		case 1:
      			if(sel2 == 1){ 		// Sel2 is iqual to activate capture function
      	 			capture = true;
      	 			loops = false;
      			}else{
      				capture = false;
      				loops = true;
      			}
        		break;
      		case 2:
        		Serial.print("T>");
        		Serial.print(sel2);  // Sel2 is iqual to minutes
        		Serial.println(">");
        		break;
      		case 3:
        		Serial.println("f");
        		break;
    	}
  	}
}

void led_blink_and_read(){
	while(loops && capture == false){
		if(micros() >= time_count && uno){
		    uno = false;
		    dos = true;
		    time_count = micros() + 5e5;
		    digitalWrite(Pin_Led_Control, 0);
		}

    	if(micros() >= time_count && dos){
      		uno = true;
      		dos = false;
      		time_count = micros() + 5e5;
      		digitalWrite(Pin_Led_Control, 1);
    	}

    	read_data();
  	}
}
