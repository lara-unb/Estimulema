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

void setup() {
  // join I2C bus (I2Cdev library doesn't do this automatically)
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
  Wire.begin();
#elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
  Fastwire::setup(400, true);
#endif
  Serial.begin(2000000);
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
  digitalWrite(Pin_Led_Control,0);

  loops_led();
}

void loop() {
  if(capture == false){
    loops = true;
    loops_led();
  }

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
      //Serial.print(pint ? String(micros()) + ";" : "0;");
      Serial.print("0;");
      accel.getAcceleration(&ax, &ay, &az);
      Serial.print(ax);
      Serial.print(";");
      Serial.print(ay);
      Serial.print(";");
      Serial.print(az);
      Serial.print(";");
      Serial.println(pint);      
    }  
    //Serial.print("a");
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

