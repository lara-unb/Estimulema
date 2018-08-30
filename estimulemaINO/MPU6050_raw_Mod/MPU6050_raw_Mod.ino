#include "I2Cdev.h"
#include "MPU6050.h"
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include "Wire.h"
#endif

#define Pin_Inter 23
#define Pin_Led_Control 13
#define Pin_signal_Control 20

MPU6050 accel;

int16_t ax = 0, ay = 0, az = 0;
bool capture = false, loops = true;
int pint = 0;

bool uno = true, dos = false; 
int co = 0;

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
  //Serial.println("Initializing I2C devices...");
  //accelgyro.initialize();
  accel.initialize();
  //Serial.println("Testing device connections...");
  //Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
  //Serial.println(accel.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
  
  pinMode(Pin_Inter, INPUT);
  pinMode(Pin_signal_Control, INPUT_PULLUP);
  pinMode(Pin_Led_Control, OUTPUT);
  attachInterrupt(Pin_Inter, Communication_data, CHANGE);
  
  digitalWrite(Pin_Led_Control,1);

  //loops_led();
}

void loop() {
  time_count = micros() + 5e5;

  while(capture == false){
    if(micros() >= time_count && uno){
      Serial.print("valor: ");
      Serial.println(co);
      co += 1;
      uno = false;
      dos = true;
      time_count = micros() + 5e5;
      digitalWrite(Pin_Led_Control, 0);
    }

    if(micros() >= time_count && dos){
      Serial.print("valor: ");
      Serial.println(co);
      co += 1;
      uno = true;
      dos = false;
      time_count = micros() + 5e5;
      digitalWrite(Pin_Led_Control, 1);
    }

    read_data();
  }

  // digitalWrite(Pin_Led_Control, 1);  

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

void Communication_data(){
  loops = false;
  capture = !capture;
}

void loops_led(){
  while(loops){
      digitalWrite(Pin_Led_Control,1);
      delay(300);
      digitalWrite(Pin_Led_Control,0);
      delay(200);
  }
}

void read_data(){

  if(Serial.available() != 0){
      char input = Serial.read();
      int input2 = (int)input - '0';

      Serial.print("Input: ");
      Serial.println(input2);

      switch (input2) {
        case 1:
          //loops = false;
          capture = !capture;
          //Serial.print("Número 1");
          break;
        case 2:
          //loops = false;
          Serial1.println("1");
          Serial.println("Número 2");  
          /*if(Serial1.available() != 0){
          }*/
          delay(5000);  
          break;
        case 3:
          //loops = false;
          Serial.println("Número 3");
          break;
      }
    }
}
