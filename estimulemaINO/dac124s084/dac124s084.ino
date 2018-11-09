#include <SPI.h>

#define DAC_SS_PIN 10

//#define CH1_MAX_POS 2047
//#define CH1_MIN_NEG 2047
#define STIM_ZERO 2047

#define cs '>'

#define RELAY_CH_1 6
#define RELAY_CH_2 7

#define Pin_Inter 23 

int MAX_POS = 2047;
int MIN_NEG = 2047;
int channel_dac = 0;

int mA = 100;
long pw = 500;
long pw_r = 19000;
bool loop_control = true;

void setup(){
	Serial.begin(2000000);

	pinMode(DAC_SS_PIN, OUTPUT);
	digitalWrite(DAC_SS_PIN, 1);

	pinMode(RELAY_CH_1, OUTPUT);
  	pinMode(RELAY_CH_2, OUTPUT);

    digitalWrite(RELAY_CH_1, 0);
  	digitalWrite(RELAY_CH_2, 0);

  	attachInterrupt(Pin_Inter, Stop_functions, RISING);

	SPI.begin();
	zeroChannels();
}

void loop(){
	while(loop_control){
		sendStimValue(channel_dac, 1, STIM_ZERO + val_ma(mA, MAX_POS));
		delayMicroseconds(pw);
		sendStimValue(channel_dac, 1, STIM_ZERO - val_ma(mA, MIN_NEG));
		delayMicroseconds(pw);
		sendStimValue(channel_dac, 1, STIM_ZERO + 10);
		delayMicroseconds(pw_r);
		read_values();
	}
	if(loop_control == false){
		zeroChannels(); 
	}
}

void read_values(){
	if(Serial.available() != 0){
	    String data_in = Serial.readStringUntil(cs);
	    channel_dac = data_in.toInt();
	    data_in = Serial.readStringUntil(cs);
	    MAX_POS = data_in.toInt();
	    data_in = Serial.readStringUntil(cs);
	    MIN_NEG = data_in.toInt();
	    data_in = Serial.readStringUntil(cs);
	    mA = data_in.toInt();

	    if(channel_dac == 0){
			digitalWrite(RELAY_CH_1, 1);
			digitalWrite(RELAY_CH_2, 0);
		}else if(channel_dac == 1){
			digitalWrite(RELAY_CH_1, 0);
			digitalWrite(RELAY_CH_2, 1);
		}else if(channel_dac == 2){
			digitalWrite(RELAY_CH_1, 0);
			digitalWrite(RELAY_CH_2, 0);
		}
	}
}

void sendStimValue(int address, int operation_mode, uint16_t value){
	byte valueToWriteH = 0;
	byte valueToWriteL = 0;

	valueToWriteH = highByte(value);
	valueToWriteH = 0b00001111 & valueToWriteH;
	valueToWriteH = (address << 6) | (operation_mode << 4) | valueToWriteH;
	valueToWriteL = lowByte(value);
	
	digitalWrite(DAC_SS_PIN, LOW);
	SPI.transfer(valueToWriteH);
	SPI.transfer(valueToWriteL);
	digitalWrite(DAC_SS_PIN, HIGH);
}

void Stop_functions() {
  Serial.println("Interrupcion activada");
  loop_control = !loop_control;
}

long val_ma(int Am, int limit) {
  int y = 0;
  y = map(Am, 0, 100, 0, limit);
  return y;
}

void zeroChannels(){
	digitalWrite(RELAY_CH_1, 0);
  	digitalWrite(RELAY_CH_2, 0);
	sendStimValue(0, 1,(uint16_t) (STIM_ZERO + 20));
	sendStimValue(1, 1,(uint16_t) (STIM_ZERO + 20));
}
