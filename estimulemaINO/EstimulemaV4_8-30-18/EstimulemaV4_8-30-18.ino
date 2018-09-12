#include <SPI.h>

//Pins definitions
#define RELAY_CH_1 6            // Relay for CH1
#define RELAY_CH_2 7            // Relay for CH1

#define Pin_Sync_Data 8         // Start and End data capture for accelerometer

#define BuzzerPin 9             // Buzzer pin activation for status messages
#define DAC_SS_PIN 10
#define Pin_signal_Control 14   // Enable data capture
#define med_out_signal1 15      // for measure the output estimulation for ch1
#define med_out_signal2 16      // for measure the output estimulation for ch2
#define Pin_Inter 23            // Emergency Button

// Original values for DAC conversion 
#define CH1_MAX_POS 1883
#define CH1_MIN_NEG 1842
#define CH2_MAX_POS 2047
#define CH2_MIN_NEG 2047

#define STIM_ZERO 2047

#define fin '>'                 // Character separator used for split data

unsigned int pwrc = 2e6;        // Time of rest used in tests rh and cr

// For input data
String data_in;                 // General variable

// Global variables
unsigned int rh = 0, cr = 0, s_c = 1, upd = 0;
unsigned int ts = 0, freq = 0, lim_pw = 0, pw_b = 50;
unsigned int one_freq = 0;
unsigned int lim_ma_ini = 0, lim_ma_fin = 0;
unsigned long pw = 0, pw_r = 0; 
unsigned long min_t = 60e6; // Time multiplicator for minutes to us
unsigned long t_stop = 0; // End time for while's

//Control loops and if variables 
bool loop_s = true, c_cr = true;
unsigned int t_adc = 23; // Sampling time
// Calculo paso de amplitud para la rampa del ch1
float up_ma1 = 0, down_ma1 = 0;
float up_ma2 = 0, down_ma2 = 0;

//Aqui coloco las variables para saber si no hay rampa
float ramp_ch1 = 0, ramp_ch2  = 0;

// Struct for channels data
struct stimulation_parameters{
  unsigned int ch_act;
  unsigned long tn; // in us
  unsigned long tf; // in us
  float ri; // in us
  float rf; // in us
  unsigned int ma; // Hz converted on Period T in us
  unsigned long tn_s; // in us tn of uplift
};

// Initialize structure
struct stimulation_parameters * data_sp; // stimulation values for CH1

// Initialize functions
void read_dataIn();
void split_functionality();
void rheobase_chronaxie(int mA_s, int t1, int t2);
void stimulation_training(bool ch1, bool ch2);
void InitializVal_struct(int ch);
void print_dataIn();
void sendStimValue(int address, int operation_mode, uint16_t value);
long val_ma(int Am, int limit);
void Stop_functions();
void zeroChannels();

/***** adicionar las funciones que faltan ***/


// Here occurs the magic, first step
void setup() {
  // Initialize parameters for Stim-PC communication
  Serial.begin(2000000);
  Serial.setTimeout(1);
  Serial.flush();

  // Initialize parameters for Stim-Accel communication
  Serial1.begin(2000000);
  Serial1.setTimeout(1);

  // Initializa SPI comunication
  SPI.begin();

  // Initialize pins functions      Used for:
  pinMode(DAC_SS_PIN, OUTPUT);            // DAC comunication
  pinMode(Pin_Sync_Data, OUTPUT);         // Accel capture
  pinMode(Pin_signal_Control, OUTPUT);    // Signal for Rh and Cr control
  pinMode(RELAY_CH_1, OUTPUT);            // CH1 activation
  pinMode(RELAY_CH_2, OUTPUT);            // CH2 activation

  pinMode(Pin_Inter, INPUT);              // Extern interruption 
  pinMode(med_out_signal1, INPUT);        // Tenp: measure CH1 signal for security system
  pinMode(med_out_signal2, INPUT);        // Tenp: measure CH2 signal for security system

  pinMode(BuzzerPin, OUTPUT);             // Buzzer
  digitalWrite(BuzzerPin, 0);             // BUzzer config - disable

  digitalWrite(DAC_SS_PIN, 1);            // SPI disable

  digitalWrite(Pin_Sync_Data, 0);         // Sync data accel disable
  Serial1.println("1>0>");

  digitalWrite(RELAY_CH_1, 0);            // Preload 0 - load 1 for CH1 - initialize with preload 
  digitalWrite(RELAY_CH_2, 0);            // Preload 0 - load 1 for CH2i - nitialize with preload

  attachInterrupt(Pin_Inter, Stop_functions, RISING); // Extern interruption configuration

  // Initialize allocated memory for 4 structures
  // 1 and 3 for CH1
  // 2 and 4 for CH2
  data_sp = (struct stimulation_parameters *) malloc(4 * sizeof(struct stimulation_parameters));

  // Inizialite structures with 0 value
  for(int i=0; i<4; i++){
    // Function for zero values assignment
    InitializVal_struct(i);
  }

  // Allocated memory for time stop and initialize with 0
  t_stop = (unsigned long) malloc(1 * sizeof(unsigned long));
  t_stop = 0;

  // Initialize stimulation with preload 
  zeroChannels();

  // Bipp of initialization
  beep(2, 100);
}

void loop() {
  // Loops for check input data
  while (loop_s) {
    // Function for input data
    read_dataIn();
  }

  // Separate for functionality
  split_functionality();
  // Disable bipp
  digitalWrite(BuzzerPin, 0);

  // Stimulation towards preload 
  zeroChannels();

  // Return to the loops read data
  loop_s = true;
}


/**************************************************************/
/******************** Read input data *************************/
/**************************************************************/
void read_dataIn() {
  // If serial is available with data
  if (Serial.available() != 0) {
    //--------------------- Therapy time ---------------------//
    data_in = Serial.readStringUntil(fin);
    ts = data_in.toInt();
    ts = ts * min_t;

    //---------------------- Frequency -----------------------//
    data_in = Serial.readStringUntil(fin);
    freq = data_in.toInt();

    //---------------------- Pulse width ---------------------//
    data_in = Serial.readStringUntil(fin);
    pw = data_in.toInt();
    one_freq = int(1e6 / freq);

    // Calculation of pulse width time
    if(pw > 0){
      pw_r = one_freq - (pw * 2);
    }else{
      pw_r = 0;
    }

    //********************** Data for channel 1 *******************//
    //--------- Ton ----------//
    data_in = Serial.readStringUntil(fin);
    data_sp[0].tn = data_in.toInt();

    //--------- Toff ---------//
    data_in = Serial.readStringUntil(fin);
    data_sp[0].tf = data_in.toInt();

    //--------- Ramp ---------//
    data_in = Serial.readStringUntil(fin);
    data_sp[0].ri = data_in.toFloat();

    ata_in = Serial.readStringUntil(fin);
    data_sp[0].rf = data_in.toFloat();

    //------- Current --------//
    data_in = Serial.readStringUntil(fin);
    data_sp[0].ma = data_in.toInt();


    //********************** Data for channel 2 *******************//
    //--------- Ton ----------//
    data_in = Serial.readStringUntil(fin);
    data_sp[1].tn = data_in.toInt();
    
    //--------- Toff ---------//
    data_in = Serial.readStringUntil(fin);
    data_sp[1].tf = data_in.toInt();
    
    //--------- Ramp ---------//
    data_in = Serial.readStringUntil(fin);
    data_sp[1].ri = data_in.toFloat();

    data_in = Serial.readStringUntil(fin);
    data_sp[1].rf = data_in.toFloat();
    
    //------- Current --------//
    data_in = Serial.readStringUntil(fin);
    data_sp[1].ma = data_in.toInt();

    //********************** Data for tests *******************//
    //------- Rheobase limit --------//
    data_in = Serial.readStringUntil(fin);
    lim_ma_ini = data_in.toInt();

    data_in = Serial.readStringUntil(fin);
    lim_ma_fin = data_in.toInt();

    //-------- Cronaxe limit --------//
    data_in = Serial.readStringUntil(fin);
    lim_pw = data_in.toInt();

    //---------- Rheobase ----------//
    data_in = Serial.readStringUntil(fin);
    rh = data_in.toInt();

    //---------- Cronaxe ----------//
    data_in = Serial.readStringUntil(fin);
    cr = data_in.toInt();

    //********************** Data for activations *******************//
    //---------- Activation channels 1 ----------//
    data_in = Serial.readStringUntil(fin);
    data_sp[0].ch_act = data_in.toInt();

    //---------- Activation channel 2 ----------//
    data_in = Serial.readStringUntil(fin);
    data_sp[1].ch_act = data_in.toInt();

    //---- Stop control / Emergency stop -------//
    data_in = Serial.readStringUntil(fin);
    s_c = data_in.toInt();

    //------------- Update values --------------//
    data_in = Serial.readStringUntil(fin);
    upd = data_in.toInt();


    //---------- Clean buffer input  ----------//
    Serial.readString(); // Read the rest of the message
    Serial.flush();      // Wait the last byte of In/Out

    //******* End data split *******//

    ////----------------------------------------------------////

    // Fix values when exist ramp value
    ramp_ch1 = data_sp[0].ri + data_sp[0].rf;
    ramp_ch2 = data_sp[1].ri + data_sp[1].rf;

    if(ramp_ch1 > 0){
      if(ramp_ch1 <= data_sp[0].tn){
        data_sp[0].tn_s = data_sp[0].tn - ramp_ch1;
      }
    }else{
      data_sp[0].tn_s = data_sp[0].tn;
    }
      
    if(ramp_ch2 > 0){
      if(ramp_ch2 <= data_sp[1].tn){
        data_sp[1].tn_s = data_sp[1].tn - ramp_ch2;
      }
    }else{
      data_sp[1].tn_s = data_sp[1].tn;
    }

    // Pass data to structures in us
    for(int i=0; i<=1; i++){
      data_sp[i].tn = data_sp[i].tn * 1e6;
      data_sp[i].tn_s = data_sp[i].tn_s * 1e6;
      data_sp[i].tf = data_sp[i].tf * 1e6;
      data_sp[i].ri = data_sp[i].ri * 1e6;
      data_sp[i].rf = data_sp[i].rf * 1e6;
    }

    // Copy data for temporal structures, this occur just one time
    if(upd == 0){
      data_sp[2].tn = data_sp[0].tn;
      data_sp[2].tn_s = data_sp[0].tn_s;
      data_sp[2].tf = data_sp[0].tf;
      data_sp[2].ri = data_sp[0].ri;
      data_sp[2].rf = data_sp[0].rf;
      data_sp[2].ma = data_sp[0].ma;

      data_sp[3].tn = data_sp[1].tn;
      data_sp[3].tn_s = data_sp[1].tn_s;
      data_sp[3].tf = data_sp[1].tf;
      data_sp[3].ri = data_sp[1].ri;
      data_sp[3].rf = data_sp[1].rf;
      data_sp[3].ma = data_sp[1].ma;
    }

    // Stops all kinds of stimulation
    if(s_c){
      // Exit from read input data
      loop_s = false;
    }else{
      // Stop data transmision 
      digitalWrite(Pin_signal_Control, 0);

      // Stop stimulation 
      zeroChannels();

      // Return to while for input data
      loop_s = true;
    }

    // Check if input data is right
    if((data_sp[0].ch_act + data_sp[1].ch_act + rh + cr) == 0){
      // Return to while for input data
      loop_s = true; 
      Serial.println("Corrupt message or no stimulation - Try again");
    }
  }// End if serial available
}// End function read_data


/**************************************************************/
/******************** Read input data *************************/
/**************************************************************/
void split_functionality(){
  // Execute the rheobase test function
  if(rh && s_c){
    // Inicial Beep
    beep(1, 50);

    // Variables for configuratyion test 
    unsigned int ma = 0;            // Count the variable value of ma
    unsigned long ppw = 5e5;        // Fixed value of pw in rheobase test 500ms
    lim_ma_fin = lim_ma_fin + 1;            // Fix count variable for mA
    digitalWrite(Pin_Sync_Data, 1); // Start data sync
    Serial1.println("1>1>");

    /*** Print data information about test ***/
    Serial.print("0;"); 
    Serial.print(ma);
    Serial.print(";");
    Serial.println(micros());

    // Wait 2 seconds for start rheobase test
    delay(2000);

    // Start with lim_ma_ini mA value and then grows sequentially with "ma"
    ma = lim_ma_ini;

    // It does all the cycles until it's finished
    while (ma < lim_ma_fin && s_c){

      /*** Print data information about test ***/
      Serial.print("0;");
      Serial.print(ma);
      Serial.println(";0");

      /** Rheobase function for start test stimulation **/ 
      rheobase(ma, ppw, pwrc);

      // Change value for next stimulation
      ma += 1; 

      // For the last value of the sequence
      if(ma >= lim_ma_fin && s_c){

        // Stop stimulation
        zeroChannels();

        /*** Print data information about test ***/
        Serial.print("0;");
        Serial.print(ma - 1);
        Serial.print(";");
        Serial.println(micros());

        digitalWrite(Pin_Sync_Data, 0);  // Stop data sync
        Serial1.println("1>0>");

        // Stop rheobase test
        rh = 0;
      }
      
    } // end while limit ma

    // Reset variables
    lim_ma_ini = 0;
    lim_ma_fin = 0;

    // This character ends the data capture 
    Serial.println(fin);

    // Final Beep
    beep(1, 25);
  } // End if rh separation
  

  if(cr && s_c){
    // Inicial Beep
    beep(1, 50);

    ////*** Variables for configuratyion test ***////
    // calculation of signal stim value for both positive and negative
    int lim_ma_iniP = STIM_ZERO + val_ma(lim_ma_ini, CH1_MAX_POS);
    int lim_ma_iniN = STIM_ZERO - val_ma(lim_ma_ini, CH1_MIN_NEG);
    unsigned int pw_c = 0;          // Count pw value
    c_cr = true;                    // ver que hjaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    lim_pw = lim_pw + 1;            // limit for PW value

    digitalWrite(Pin_Sync_Data, 1); // Start capture in Accel Teensy
    Serial1.println("1>1>");
    
    /*** Print data information about test ***/
    Serial.print("0;");
    Serial.print(pw_c);
    Serial.print(";");
    Serial.println(micros());

    // Wait 2 seconds for start Cronaxie test
    delay(2000);

    // Temporal value
    pw_c = pw_b;

    // Set stimulation for 0
    while(pw_c < lim_pw && s_c) {
      /*** Print data information about test ***/
      Serial.print("0;");
      Serial.print(pw_c);
      Serial.println(";0");

      /** Cronaxie function for start test stimulation **/ 
      chronaxie(lim_ma_iniP, lim_ma_iniN, pw_c, pwrc);

      // Change value for next stimulation
      pw_c += pw_b;

      // For the last value of tthe sequence
      if(pw_c >= lim_pw && s_c){

        // Stop stimulation
        zeroChannels();  

        /*** Print data information about test ***/
        Serial.print("0;");
        Serial.print(pw_c - pw_b);
        Serial.print(";");
        Serial.println(micros());

        digitalWrite(Pin_Sync_Data, 0); // Stop data sync
        Serial1.println("1>0>");

        // Stop cronaxie test
        cr = 0;
      }
    } // End while limit pw

    // Reset variable
    lim_ma_ini = 0;

    // This character ends the data capture 
    Serial.println(fin);

    // final beep
    beep(1, 25);
  } // End if cr separation

  
  // for training stimulation
  if(data_sp[0].ch_act && data_sp[1].ch_act == 0 && s_c){
    /* For CH 1 */ 
    stimulation_training(1,0);
  }else if(data_sp[0].ch_act == 0 && data_sp[1].ch_act){
    /* For CH 1 */
    stimulation_training(0,1);
  }else if(data_sp[0].ch_act && data_sp[1].ch_act && s_c){
    /* For CH 1 */
    stimulation_training(1,1);
  }

  /* Resset all  variables */
  rh = 0;
  cr = 0;
  data_sp[0].ch_act = 0;
  data_sp[1].ch_act = 0;
}// End function of split funcionality


/**************************************************************/
/******************** Rheobase function ***********************/
/**************************************************************/
void rheobase(int mA_s, unsigned int t1, unsigned int t2) {
  /*
  mA_s = Current value for start test
  t1 = pulse withd for stimulation ("T_on")
  t2 = pulse withd rest ("T_off")
  */

  // Reset variable
  t_stop = 0;

  digitalWrite(RELAY_CH_1, 1);            // Enable CH1 for stimulation

  digitalWrite(Pin_signal_Control, 1);    // Enable accel for data capture

  /*** Print data information about test ***/
  Serial.print("1;");
  Serial.print(mA_s);
  Serial.print(";");
  Serial.println(micros());               // Initial value on micros

  // Start stimulation for Positive phase
  sendStimValue(0, 1, STIM_ZERO + val_ma(mA_s, CH1_MAX_POS));

  // Count the time and read the serial port to update the data
  t_stop = micros() + t1;
  while (micros() <= t_stop && s_c) {
    read_dataIn();
  }

  /*** Print data information about test ***/
  Serial.print("1;");
  Serial.print(mA_s);
  Serial.print(";");
  Serial.println(micros());

  // Start stimulation for Negative phase
  sendStimValue(0, 1, STIM_ZERO - val_ma(mA_s, CH1_MIN_NEG));

  /*** Print data information about test ***/
  Serial.print("2;");
  Serial.print(mA_s);
  Serial.print(";");
  Serial.println(micros());

  // Count the time and read the serial port to update the data
  t_stop = micros() + t1;
  while (micros() <= t_stop && s_c) {
    read_dataIn();
  }

  /*** Print data information about test ***/
  Serial.print("2;");
  Serial.print(mA_s);
  Serial.print(";");
  Serial.println(micros());
  Serial.print("0;");
  Serial.print(mA_s);
  Serial.println(";0");

  // Rest stimulation
  sendStimValue(0, 1, STIM_ZERO);

  digitalWrite(Pin_signal_Control, 0);      // Disable accel for data capture

  // Count the time and read the serial port to update the data
  t_stop = micros() + t2;
  while (micros() < t_stop && s_c) {
    read_dataIn();
  }
} // Ends rheobase function


/**************************************************************/
/******************** Cronaxie function ***********************/
/**************************************************************/
void chronaxie(int mA_sP, int mA_sN, unsigned int t1, unsigned int t2) {
  /*
  mA_sP = Positive current value for cronaxie test 
  mA_sN = Negative current value for cronaxie test
  t1 = pulse withd for stimulation ("T_on")
  t2 = pulse withd rest ("T_off")
  */

  // Reset variable
  t_stop = 0;

  digitalWrite(RELAY_CH_1, 1);              // Enable CH1 for stimulation

  digitalWrite(Pin_signal_Control, 1);      // Enable accel for data capture

  /*** Print data information about test ***/
  Serial.print("1;");
  Serial.print(mA_sP);
  Serial.print(";");
  Serial.println(micros()); // Initial value on micros

  // This states make the first stimulation signal and
  // Start stimulation for Positive phase
  if(cr && c_cr){
    sendStimValue(0, 1, STIM_ZERO + 1);
    c_cr = false;
  }else{
    sendStimValue(0, 1, mA_sP);
  }

  // Count the time and read the serial port to update the data
  t_stop = micros() + t1;
  while (micros() < t_stop && s_c) {
    read_dataIn();
  }

  /*** Print data information about test ***/
  Serial.print("1;");
  Serial.print(mA_sP);
  Serial.print(";");
  Serial.println(micros());
  Serial.print("2;");
  Serial.print(mA_sN);
  Serial.print(";");
  Serial.println(micros());

  // Start stimulation for Negative phase
  sendStimValue(0, 1, mA_sN);

  // Count the time and read the serial port to update the data
  t_stop = micros() + t1;
  while (micros() < t_stop && s_c) {
    read_dataIn();
  }

  /*** Print data information about test ***/
  Serial.print("2;");
  Serial.print(mA_sN);
  Serial.print(";");
  Serial.println(micros());
  Serial.print("0;0;0");

  // Rest stimulation
  sendStimValue(0, 1, STIM_ZERO);

  digitalWrite(Pin_signal_Control, 0);      // Disable accel for data capture

  // Count the time and read the serial port to update the data
  t_stop = micros() + t2;
  while (micros() < t_stop && s_c) {
    read_dataIn();
  }
} // Ends cronaxie function


/**************************************************************/
/******************** Cronaxie function ***********************/
/**************************************************************/
void stimulation_training(int ch1, int ch2){

  beep(1, 100);

  // Variables para el ts
  unsigned long ts_micros = 0;

  bool B_i = false;                                 // For buzzer control
  unsigned long min_elapsed = 0, Buzzer_Ini = 0;    // Control notification sound

  // For sound activation and minutes count
  min_elapsed = min_t + micros();
  int cont_s = 0;   

  // variables para ton y toff para ch1
  unsigned long t_tn1 = 0;
  unsigned long t_tf1 = 0;

  // CONTADOR TIEMPO PARA LA RAMPA DOWN E UP
  unsigned long t_ru = 0, t_rd = 0;
  
  bool ls_ltf1 = 1;
  bool lts1 = 1; // variable de control loop ton y toff par ch 1
  bool ramp_1u = 1; // var control loop rampa subida
  bool ramp_1d = 0; // var control loop rampa bajada

  bool lr1 = 0;  // var control sinal loop + rampa
  bool lrm1 = 0; // var control sinal loop - rampa
  bool lrf1 = 0; // var control pw_r da rampa
  bool ls1 = 0;  // var control loop sustentacion

  bool lsp1 = 0;  // var control signal loop + sustentacion
  bool lsn1 = 0;  // var control signal loop - sustentacion
  bool lsr1 = 0;  // var control signal loop rest sustentacion

  // var tiempo pw para ramp +/- y los pulsos +/-
  unsigned long t_pw1 = 0;
  unsigned long t_pw_r1 = 0;
  unsigned long t_tn_s = 0;

  // var auxiliar para convertir valor float a a entero de la var anterior
  // up y down
  float ma_u1 = 0, ma_d1 = 0;

  if (data_sp[0].ri > 0){
    float div = data_sp[0].ri / one_freq; // divido el tiempo en la fequencia
    up_ma1 = data_sp[0].ma / div; // valor de paso de mA segun el tiempo
    ramp_1u = 1;
  }else{
    ramp_1u = 0;
    ma_u1 = data_sp[0].ma;
  } 

  if (data_sp[0].rf > 0){
    float div = data_sp[0].rf / one_freq; // divido el tiempo en la fequencia
    down_ma1 = data_sp[0].ma / div; // valor de paso de mA segun el tiempo
    ramp_1d = 1;
  }else{
    ramp_1d = 0;
    ma_d1 = 0;
  } 

  // Setando los valores iniciales
  unsigned long t_ts_cal = ts;
  ts_micros = micros();
  unsigned long t_ini_temp = ts_micros;
  t_stop = micros() + ts;


  // habilita el canal 1 para salida
  if(ch1){
    Tempo valores y activaciones para canal 1
    t_tn1 = micros() + data_sp[0].tn;
    t_pw1 = micros() + pw;
    t_ru = micros() + data_sp[0].ri; // actualiza el valor de la duracion de la rampa
    t_rd = micros() + data_sp[0].rf; // actualiza el valor de la duracion de la rampa

    digitalWrite(RELAY_CH_1, 1);
  }
  
  // Here occur the magic for therapy stimulation
  while(ts_micros < t_stop){

    // ramp up ch1
    if(lts1 && ramp_1u){ // colocar verificacion para inicio y fin
      if(micros() <= t_ru && ma_u1 < data_sp[0].ma){
        if(micros() >= t_pw1 && lr1 == 0 ){
          sendStimValue(0, 1, STIM_ZERO - val_ma(ma_u1, CH1_MIN_NEG));
          lr1 = 1;
          lrm1 = 1;
          t_pw1 = micros() + pw; // actualiza el valor de pw
        }else if(micros() >= t_pw1 && lrm1){
          sendStimValue(0, 1, STIM_ZERO + 1);
          lrf1 = 1;
          lrm1 = 0;
          t_pw_r1 = micros() + pw_r; // actualiza el valor de pw
        } else if(micros() >= t_pw_r1 && lrf1){
          ma_u1 +=  up_ma1;
          sendStimValue(0, 1, STIM_ZERO + val_ma(ma_u1, CH1_MAX_POS));
          lrf1 = 0;
          lr1 = 0;
          t_pw1 = micros() + pw; // actualiza el valor de pw
        }
      }else{ // si ya paso el tiempo de la rampa o llegó al valor
        ls1 = 1; // habilita sustentacion sustentacion
        lsp1 = 0;
        sendStimValue(0, 1, STIM_ZERO + val_ma(data_sp[0].ma, CH1_MAX_POS));
        // Actualiza tiempos para tempo de
        if(data_sp[0].rf > 0){
          t_tn_s = micros() + data_sp[0].tn_s - ; // actualiza tiempo sustentacion        
        } else{
          t_tn_s = micros() + data_sp[0].tn_s; // actualiza tiempo sustentacion
        }
        // inicia el componente positivo
        t_pw1 = micros() + pw; // actualiza el valor de pw
      }
    }else if(ls_ltf1){
      ls1 = 1; // habilita sustentacion sustentacion
      lsp1 = 0;
      sendStimValue(0, 1, STIM_ZERO + val_ma(data_sp[0].ma, CH1_MAX_POS));
      // Actualiza tiempos para tempo de 
      t_tn_s = micros() + data_sp[0].tn_s; // actualiza tiempo sustentacion
      // inicia el componente positivo
      t_pw1 = micros() + pw; // actualiza el valor de pw
    }

    // For positive stimulation in ch1
    if(lts1 && ls1){ // Sustentacion
      if(micros() <= t_tn_s){
        //Serial.println("Entra ciclo 1");
        if(micros() >= t_pw1 && lsp1 == 0){
          sendStimValue(0, 1, STIM_ZERO - val_ma(data_sp[0].ma, CH1_MIN_NEG));
          lsp1 = 1;
          lsn1 = 1;
          t_pw1 = micros() + pw; // actualiza el valor de pw
        }else if(micros() >= t_pw1 && lsn1){
          sendStimValue(0, 1, STIM_ZERO + 1);
          lsr1 = 1;
          lsn1 = 0;
          t_pw_r1 = micros() + pw_r; // actualiza el valor de pw
        }else if(micros() >= t_pw_r1 && lsr1){
          sendStimValue(0, 1, STIM_ZERO + val_ma(data_sp[0].ma, CH1_MAX_POS));
          lsr1 = 0;
          lsp1 = 0;
          t_pw1 = micros() + pw; // actualiza el valor de pw
        }
      }else{
        if(data_sp[0].rf > 0){
          ramp_1d = 1;
          ma_d1 = data_sp[0].ma;
          sendStimValue(0, 1, STIM_ZERO + val_ma(ma_u1, CH1_MAX_POS));
          lr1 = 0;
          lrm1 = 0;
          lrf1 = 0;
          t_r = micros() + data_sp[0].r; // actualiza el valor de la duracion de la rampa
          t_pw1 = micros() + pw; // actualiza el valor de pw
        }else{ // termin el ciclo de tn y habilita tf
          ramp_1d = 0;
          ls1 = 1;
          lts1 = 0;
          t_tf1 = micros() + data_sp[0].tf;
        }       
      }
    }

    // ramp down ch1
    if(lts1 && ramp_1d){ // colocar verificacion para inicio y fin
      if(micros() <= t_r && ma_d1 > 0){
        if(micros() >= t_pw1 && lr1 == 0){
          sendStimValue(0, 1, STIM_ZERO - val_ma(ma_u1, CH1_MIN_NEG));
          lr1 = 1;
          lrm1 = 1;
          t_pw1 = micros() + pw; // actualiza el valor de pw
        } else if(micros() >= t_pw1 && lrm1){
          sendStimValue(0, 1, STIM_ZERO + 1);
          lrm1 = 0;
          lrf1 = 1;
          t_pw_r1 = micros() + pw_r; // actualiza el valor de pw
        }else if(micros() >= t_pw_r1 && lrf1){
          ma_u1 -=  up_down_ma1;
          sendStimValue(0, 1, STIM_ZERO + val_ma(ma_u1, CH1_MAX_POS));
          lrf1 = 0;
          lr1 = 0;
          t_pw1 = micros() + pw; // actualiza el valor de pw
        }
      }else{
        if cotrol re marcion de parametros

        sendStimValue(0, 1, STIM_ZERO + 1); // cera la salida
        lr1 = 0;
        ma_u1 = 0;
        if(data_sp[0].r == 0){
          ramp_1u = 0;
          ramp_1d = 0;
        }else{
          ramp_1d = 0;
          ramp_1u = 1;
        }
        lts1 = 0;
        ma_u1 = 0;
        t_tf1 = micros() + data_sp[0].tf;
      }
    }

    // For Tf in Ch1
    if(lts1 == 0){
      //zeroChannels();
      digitalWrite(RELAY_CH_1, 0);
      if(micros() >= t_tf1 && ch1){
        digitalWrite(RELAY_CH_1, 1);
        lts1 = 1;
        t_tn1 = micros() + data_sp[0].tn;
        t_r = micros() + data_sp[0].r;
        t_pw1 = micros() + pw;
        ma_u1 = 0;
      }
    }

    // Verify the time for every minute
    if(micros() >= min_elapsed){
      Serial.println("m");
      cont_s += 1;
      min_elapsed = min_t + micros();
      B_i = true;
      digitalWrite(BuzzerPin, 1); // Enable pin buzzer
      Buzzer_Ini = 2e5 + micros();
      Serial1.print("2>");
      Serial1.print(cont_s);
      Serial1.println(">");
    }

    // Activate the buzzer sequence
    if (micros() >= Buzzer_Ini && B_i) {
      digitalWrite(BuzzerPin, 0); // Disable pin buzzer
      B_i = false;
    }

    if(s_c == 0){
      t_stop = ts_micros;
    }



    // Read imput data for update values
    read_dataIn();

  // Update values
    if(upd){ 
      sendStimValue(0, 1, STIM_ZERO);
      sendStimValue(1, 1, STIM_ZERO);

      // Update time therapy
      unsigned long t_ts_cal_temp = ts; // nuevo valor entrando
      if(t_ts_cal != t_ts_cal_temp){
        if(t_ts_cal < t_ts_cal_temp){
          t_stop = t_ini_temp + t_ts_cal_temp;
        } 
        if((ts_micros - t_ini_temp) < (t_ini_temp + t_ts_cal_temp)) {
          t_stop = t_ini_temp + t_ts_cal_temp;
        } else{
          s_c = 0;
        }
      }

      // Activation/Deactivation of channel
      if(data_sp[0].ma == 0){
        ch1 = 0;
      }else if(data_sp[0].ch_act && data_sp[0].ma > 0){
        ch1 = 1;
      }

      if(data_sp[1].ma == 0){
        ch2 = 0;
      }else if(data_sp[1].ch_act && data_sp[1].ma > 0){
        ch2 = 1;
      }
      
      // For stop stimulation or emergency stop
      if(data_sp[0].ma == 0 && data_sp[1].ma == 0){
        Serial.println("Parada de emergencia");
        s_c = 0; 
        // Stop stimulation
        zeroChannels();
      }
      
      // Current Update 
      if(data_sp[0].ma != data_sp[2].ma){
        if (lsp1 == 0){
          sendStimValue(0, 1, STIM_ZERO + val_ma(data_sp[0].ma, CH1_MAX_POS));
        } else if (lsn1){
          sendStimValue(0, 1, STIM_ZERO - val_ma(data_sp[0].ma, CH1_MIN_NEG));
        }
        data_sp[2].ma = data_sp[0].ma;
      }

      /*if(data_sp[1].ma != data_sp[3].ma){
        if (lp1 == 0 && ln1 && lf1){
          sendStimValue(1, 1, STIM_ZERO + val_ma(data_sp[1].ma, CH2_MAX_POS));
        } else if (ln1 == 0 && lf1){
          sendStimValue(1, 1, STIM_ZERO - val_ma(data_sp[1].ma, CH2_MIN_NEG));
        }
        data_sp[3].ma = data_sp[1].ma;
      }*/

      if(data_sp[0].r == 0){
        ramp_1u = 0;
        ramp_1d = 0;
      }else{
        ramp_1u = 1;
      }

      if (data_sp[0].r > 0){
        float div = data_sp[0].r / one_freq; // divido el tiempo en la fequencia
        up_down_ma1 = data_sp[0].ma / div; // valor de paso de mA segun el tiempo
      }else{
        ma_u1 = data_sp[0].ma;
      }
      
      upd = 0; // desactivo la actualizacion
      ma_u1 = 0;
    } // Fin update


  ts_micros = micros(); // Update micros variable
}// End while update

  // End character for identify finish or stop stimulation
  Serial1.println("3>0>");

  Serial.println("Fin");

  // Bipp for end or stop stimulation
  beep(0, 200);

  // Stop stimulation
  zeroChannels();
}// Ends therapy function


void InitializVal_struct(int ch){
  // For data of stimulation parameters
  data_sp[ch].ch_act = 0;
  data_sp[ch].tn = 0;
  data_sp[ch].tf = 0;
  data_sp[ch].r = 0;
  data_sp[ch].ma = 0;
  data_sp[ch].tn_s = 0;
}


/**************************************************************/
/**************** DAC Communication function ******************/
/**************************************************************/
void sendStimValue(int address, int operation_mode, uint16_t value) {
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


/**************************************************************/
/********* Converter data function for DAC value **************/
/**************************************************************/
long val_ma(int Am, int limit) {
  //Serial.print("Valor mA: ");
  //Serial.println(Am);
  int y = 0;
  y = map(Am, 0, 100, 0, limit);
  return y;
}

/**************************************************************/
/********************* Stop everything ************************/
/**************************************************************/
void Stop_functions() {
  // Stop stimulation
  zeroChannels();

  s_c = 0;
  data_sp[0].ma = 0;
  data_sp[1].ma = 0;
  digitalWrite(Pin_Sync_Data, 0);         // Control sigal for Accel
  Serial1.println("1>0>");

  digitalWrite(Pin_signal_Control, 0);    // Enable capture for data control
}


/**************************************************************/
/********************* Stop stimulation ***********************/
/**************************************************************/
void zeroChannels() {
  digitalWrite(RELAY_CH_1, 0);
  digitalWrite(RELAY_CH_2, 0);
  sendStimValue(0, 1, (uint16_t) (STIM_ZERO + 10));
  sendStimValue(1, 1, (uint16_t) (STIM_ZERO + 10));
}


/**************************************************************/
/********************* Stop stimulation ***********************/
/**************************************************************/
void beep(int sel, int t){
  if(sel == 2){
    digitalWrite(BuzzerPin, 1);
    delay(500);
    digitalWrite(BuzzerPin, 0);
    delay(100);
    digitalWrite(BuzzerPin, 1);
    delay(100);
    digitalWrite(BuzzerPin, 0);
  }

  if(sel){
    digitalWrite(BuzzerPin, 1);
    delay(t*3);
    digitalWrite(BuzzerPin, 0);
    delay(t);
    digitalWrite(BuzzerPin, 1);
    delay(t);
    digitalWrite(BuzzerPin, 0);
  }

  if(sel == 0){
    digitalWrite(BuzzerPin, 1);
    delay(t);
    digitalWrite(BuzzerPin, 0);
    delay(t);
    digitalWrite(BuzzerPin, 1);
    delay(t);
    digitalWrite(BuzzerPin, 0);
    delay(t);
    digitalWrite(BuzzerPin, 1);
    delay(t);
    digitalWrite(BuzzerPin, 0);
  }

}


void print_dataIn(){
  String msg = "";

  msg = String(ts) + fin + String(freq) + fin + String(pw) + fin ;
  //ch1
  msg = msg + String(data_sp[0].tn) + fin + String(data_sp[0].tf) + fin + String(data_sp[0].r) + fin + String(data_sp[0].ma);
  //ch1
  msg = msg + fin + String(data_sp[1].tn) + fin + String(data_sp[1].tf) + fin + String(data_sp[1].r) + fin + String(data_sp[1].ma);
  //limits
  msg = msg + fin + String(lim_ma_ini) + fin + String(lim_ma_fin) + fin + String(lim_pw) + fin;
  //activation
  msg = msg + String(rh) + fin + String(cr) + fin + String(data_sp[0].ch_act) + fin + String(data_sp[1].ch_act) + fin;
  //stop
  msg = msg + String(s_c) + fin + String(upd) + "> -- " + String(pw_r);

  Serial.println(msg);
  Serial.print("");
  Serial.print("");
  Serial.print("");
  Serial.print("");
}
