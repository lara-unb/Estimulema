#include "HX711.h"

// HX711 circuit wiring
//const int DOUT_PIN = 2; 
//const int SCK_PIN = 3;

const int DOUT_PIN = 22; 
const int SCK_PIN = 23;

bool uno = true, dos = false; 
unsigned long time_count = 0;

//float calibration_factor = 39500; // this calibration factor is adjusted according to my load cell 39500 com com11
float calibration_factor = 39500; // this calibration factor is adjusted according to my load cell 51000 com10

float units;
bool loops = true;

HX711 scale;

void setup() {
  Serial.begin(2000000);
  scale.begin(DOUT_PIN, SCK_PIN);
  scale.set_scale();
  scale.tare();  //Reset the scale to 0
}

void loop() {
  while(loops){
    read_port();
  }

  Serial.print(micros());
  Serial.print(";");
  scale.set_scale(calibration_factor); 
  units = scale.get_units(), 1;
  units = units * -1;
  if (units < 0){
    units = 0.00;
  }
  Serial.println(units);

  while(loops == false){
    scale.set_scale(calibration_factor); 
    units = scale.get_units(), 1;
    units = units * -1;
    if (units < 0){
      units = 0.00;
    }
    Serial.print("0;");
    Serial.println(units);
    read_port();
  }

  Serial.print(micros());
  Serial.print(";");
  scale.set_scale(calibration_factor); 
  units = scale.get_units(), 1;
  units = units * -1;
  if (units < 0){
    units = 0.00;
  }
  Serial.println(units);

  //delay(100);
  
}

void read_port(){
  if (Serial.available() != 0) {
      String car_ini = Serial.readString();
      //Serial.println(car_ini);
      //Serial.readString();
      if(car_ini == "s"){
        loops = false;
      }else{
        loops = true;
      }
  }
}

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

    	read_port();
  	}