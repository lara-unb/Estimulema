#define pin_led 13
#define pin_dac A14
#define pin_adc A14


#define STIM_ZERO 2047
#define fin '>'

// For data in
String data_in; 
unsigned int rh = 0, cr = 0, s_c = 1, upd = 0, t_adc = 23;
unsigned int ts = 0, freq = 0, lim_ma = 0, lim_pw = 0, pw_b = 50;
unsigned long pw = 0, pw_r = 0; 
unsigned long min_t = 60e6; // multiplicador tempo para min a us

bool loop_s = true;

struct stimulation_parameters{
  unsigned int ch_act;
  unsigned long tn; // in useconds
  unsigned long tf;
  unsigned long r;
  unsigned int ma; // Hz converted on Period T in us
};

struct stimulation_parameters * data_sp; // stimulation values for CH1

int t = 100;

void setup() {
  Serial.begin(2000000);
  Serial.setTimeout(1);
  Serial.flush();

  pinMode(pin_led, OUTPUT)  ;
  digitalWrite(pin_led, 0);
  analogWriteResolution(12);

  data_sp = (struct stimulation_parameters *) malloc(2 * sizeof(struct stimulation_parameters));
  for(int i=0; i<2; i++){
    InitializVal_struct(1);
  }

  analogWrite(pin_dac, STIM_ZERO); //cinfigurando el dac
  pinMode(pin_adc, INPUT); //configurando adc pin

}

void loop() {
  while (loop_s) {
    read_dataIn();
  }

  stimulation_training();

  loop_s = true;
}

void blinkar(int time_blink){  
  digitalWrite(pin_led,1);
  delay(time_blink);
  digitalWrite(pin_led,0);
  delay(time_blink * 2);
}

void stimulation_training(){
  
  //for signal control
  ts = 10;
  data_sp[0].tn = 5;
  s_c = 1;
  data_sp[0].tf = 0;
  pw = 5000 - t_adc;

  unsigned long t_stop = 0, t_ini_temp = 0;
  bool lp1 = 1, ln1 = 1, lr1 = 1, lf1 = 1;

  bool tn1 = 1;
  unsigned long t_tn1 = 0, t_tf1 = 0;
  unsigned long t_pnfl1 = 0, t_pw_2 = int(pw / 2);
  unsigned long t_ts_temp = 0, t_ts_cal = 0, t_ts_cal_temp = 0;

  unsigned long seg10 = 0;

  //Inicializo variables
  t_ts_cal = ts * min_t;
  t_stop = micros() + t_ts_cal;
  t_tn1 = micros() + data_sp[0].tn;
  t_ts_temp = micros();
  t_ini_temp = t_ts_temp; // para actualizar tiempo de terapia

  //Para testar seg en el while de ts
  seg10 = 1e6 + micros();
  int cont_s = 0;

  while(t_ts_temp < t_stop && s_c){
    // for Tn
    if(micros() >= t_tn1 && tn1 && upd == 0 && s_c){
      tn1 = 0;
      t_tf1 = micros() + data_sp[0].tf;
    }
    // for tf
    if(micros() >= t_tf1 && tn1 == 0 && upd == 0 && s_c){
      t_tn1 = micros() + data_sp[0].tn;
      tn1 = 1;
    }
    //Para el lado possitivo
    if(micros() <= t_tn1 && lp1 && s_c && upd == 0){
      analogWrite(pin_dac, STIM_ZERO + data_sp[0].ma);
      lp1 = 0;
      lf1 = 1;
      t_pnfl1 = micros() + pw;
    }
    // verificar sinal analogico
    if(lp1 == 0 && micros() <= t_pw_2){
      int v_m1 = analogRead(pin_adc);
      int v_m2 = analogRead(pin_adc);
      int v_m3 = analogRead(pin_adc);
      if(data_sp[0].ma < 3){
        v_m1 = v_m1 * 10;
        v_m2 = v_m2 * 10;
        v_m3 = v_m3 * 10;
      }else if(data_sp[0].ma > 3 && data_sp[0].ma < 10){
        v_m1 = v_m1 * 2;
        v_m2 = v_m2 * 2;
        v_m3 = v_m3 * 2;
      }
      v_mf = int((v_m1 + v_m2 + v_m3) / 3 );
    }
    //Para el lado Negativo
    if(micros() <= t_tn1 && micros() >= t_pnfl1 && lp1 == 0 && ln1 && s_c && upd == 0){
      analogWrite(pin_dac, STIM_ZERO - data_sp[0].ma);
      ln1 = 0;
      t_pnfl1 = micros() + pw;
    }
    //Para el lado Rest
    if(micros() <= t_tn1 && micros() >= t_pnfl1 && ln1 == 0 && lr1 && s_c && upd == 0){
      analogWrite(pin_dac, STIM_ZERO);
      lr1 = 0;
      t_pnfl1 = micros() + pw_r;
    }
    // reset final
    if(micros() <= t_tn1 && micros() >= t_pnfl1 && lr1 == 0 && lf1 && s_c && upd == 0){
      lf1 = 0;
      lp1 = 1;
      ln1 = 1;
      lr1 = 1;
    }
    read_dataIn();
    if(upd){ //si upd = 1 há atualização
      analogWrite(pin_dac, STIM_ZERO);

    //Actualizacion de corriente
    if(data_sp[0].ma != data_sp[2].ma){
        //Serial.println("Actualiza mA ch1");
        if (lp1 == 0 && ln1 && lf1){
          analogWrite(pin_dac, STIM_ZERO + data_sp[0].ma);
        } else if (ln1 == 0 && lf1){
          analogWrite(pin_dac, STIM_ZERO - data_sp[0].ma);
        }
        data_sp[2].ma = data_sp[0].ma;
      }

      upd = 0; // desactivo la actualizacion
    } // Fin update

  t_ts_temp = micros(); //update micros
  }//fin while uppdate

}

void InitializVal_struct(int ch){
  // For data of stimulation parameters
  data_sp[ch].ch_act = 0;
  data_sp[ch].tn = 0;
  data_sp[ch].tf = 0;
  data_sp[ch].r = 0;
  data_sp[ch].ma = 0;
}

void read_dataIn() {
  if (Serial.available() != 0) {
    //-----------------------------------------------------------------/
    //Therapy time
    data_in = Serial.readStringUntil(fin);
    //Frequency
    data_in = Serial.readStringUntil(fin);
    //Pulse width
    freq = 10;
    data_in = Serial.readStringUntil(fin);
    pw = 50000;
    if(pw > 0){
      pw_r = int(1e6 / freq) - (pw * 2);
    }else{
      pw_r = 0;
    }
    //-----------------------------------------------------------------/
    /* for channel 1 */
    // Ton
    data_in = Serial.readStringUntil(fin);
    // Toff
    data_in = Serial.readStringUntil(fin);
    // Ramp
    data_in = Serial.readStringUntil(fin);
    // Current
    data_in = Serial.readStringUntil(fin);
    data_sp[0].ma = data_in.toInt();
    //-----------------------------------------------------------------/
    /* for channel 2 */
    // Ton
    data_in = Serial.readStringUntil(fin);
    // Toff
    data_in = Serial.readStringUntil(fin);
    // Ramp
    data_in = Serial.readStringUntil(fin);
    // Current
    data_in = Serial.readStringUntil(fin);
    //-----------------------------------------------------------------/
    /* for tests */
    // for Rheobase limit
    data_in = Serial.readStringUntil(fin);
    // for Cronaxe limit
    data_in = Serial.readStringUntil(fin);
    // for Rheobase
    data_in = Serial.readStringUntil(fin);
    // for Cronaxe
    data_in = Serial.readStringUntil(fin);
    //-----------------------------------------------------------------/
    /* for Activations */
    // Channels 1 e 2
    data_in = Serial.readStringUntil(fin);
    // for Cronaxe
    data_in = Serial.readStringUntil(fin);
    data_in = Serial.readStringUntil(fin);
    data_in = Serial.readStringUntil(fin);
    upd = data_in.toInt();
    Serial.readString();//limpia buffer 
    Serial.flush();//espera hasta el ultimo byte de In Out 

    int i = 0;
    data_sp[i].tn = data_sp[i].tn * 1e6;
    data_sp[i].tf = data_sp[i].tf * 1e6;
    data_sp[i].r = data_sp[i].r * 1e6;

    if(s_c){
      loop_s = false;
    }else{ //Solo si activa el stop control
      loop_s = true;
    }

    //Serial.println("pasando datos a las estructuras temporales");
    int ch_t = 1;
    if(upd == 0){ //Solo la primera vez funciona
      data_sp[ch_t].tn = data_sp[0].tn;
      data_sp[ch_t].tf = data_sp[0].tf;
      data_sp[ch_t].r = data_sp[0].r;
      data_sp[ch_t].ma = data_sp[0].ma;
    }

  }// fin if serial avaliable
}// fin function