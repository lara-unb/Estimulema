#define p0 A0
#define p14 A14

int vol = 0, ref = 100;

void setup() {
  Serial.begin(2000000);
  analogWriteResolution(12);
  //vol = map(100, 0, 100, 0, 4095);
  analogWrite(p14, 0);
}

void loop() {
  if(Serial.available() != 0){
    String sel = Serial.readString();
    int sel_int = sel.toInt();

    if(sel_int == 1){
      medir_read_adc();
    }
    if(sel_int == 2){
      medir_read_adc_proceso_comparacion();
    }
    if(sel_int == 3){
      teste_adc();
    }      
  }
}

void medir_read_adc(){
   for(int i = 0; i < 10; i++){
    Serial.println(micros());
    int a = analogRead(p0);
    Serial.println(a);
    Serial.println(micros());
   }
}

void medir_read_adc_proceso_comparacion(){
  ref = 50;
  vol = map(ref, 0, 3250, 0, 4095);
  analogWrite(p14, vol);
  Serial.println(micros());
  int v_m1 = analogRead(p0);
  Serial.println(v_m1);      
  int v_m2 = analogRead(p0);
  int v_m3 = analogRead(p0);

  if(ref < 120){        
    v_m1 = v_m1 * 10;
    Serial.println(v_m1);
    v_m2 = v_m2 * 10;
    v_m3 = v_m3 * 10;
    int v_mf = v_m1 + v_m2 + v_m3;
    v_mf = int(v_mf/3);

    Serial.println("Valor medio: ");
    Serial.println(v_mf);

    if(v_mf >= 280){ // 280 = 900mV
      Serial.println("pasa * 10");
    }else{
      Serial.println("No pasa * 10");
    }
  }
  if(ref > 200 && ref < 900){
    v_m1 = v_m1 * 2;
    v_m2 = v_m2 * 2;
    v_m3 = v_m3 * 2;
    int v_mf = v_m1 + v_m2 + v_m3;
    v_mf = int(v_mf/3);

    Serial.println("Valor medio: ");
    Serial.println(v_mf);

    if(v_mf >= 280){ // 280 = 900mV
      Serial.println("pasa * 2");
    }else{
      Serial.println("No pasa * 2");
    }
  }
  Serial.println(micros());
}

void teste_adc(){
  analogWrite(p14, 126);
  int val = analogRead(p0);
  Serial.println("Valor leido: ");
  Serial.println(val);
}

