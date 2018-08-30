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
unsigned int lim_ma_ini = 0, lim_ma_fin = 0;
unsigned long pw = 0, pw_r = 0; 
unsigned long min_t = 60e6; // Time multiplicator for minutes to us
unsigned long t_stop = 0; // End time for while's

//Control loops and if variables 
bool loop_s = true, c_cr = true;
unsigned int t_adc = 23; // Sampling time

// Struct for channels data
struct stimulation_parameters{
  unsigned int ch_act;
  unsigned long tn; // in useconds
  unsigned long tf;
  unsigned long r;
  unsigned int ma; // Hz converted on Period T in us
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
  digitalWrite(BuzzerPin, 1);
  delay(500);
  digitalWrite(BuzzerPin, 0);
  delay(250);
  digitalWrite(BuzzerPin, 1);
  delay(125);
  digitalWrite(BuzzerPin, 0);
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

    //---------------------- Frequency -----------------------//
    data_in = Serial.readStringUntil(fin);
    freq = data_in.toInt();

    //---------------------- Pulse width ---------------------//
    data_in = Serial.readStringUntil(fin);
    pw = data_in.toInt();

    // Calculation of pulse width time
    if(pw > 0){
      pw_r = int(1e6 / freq) - (pw * 2);
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
    data_sp[0].r = data_in.toInt();

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
    data_sp[1].r = data_in.toInt();
    
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

    // Pass data to structures in us
    for(int i=0; i<=1; i++){
      data_sp[i].tn = data_sp[i].tn * 1e6;
      data_sp[i].tf = data_sp[i].tf * 1e6;
      data_sp[i].r = data_sp[i].r * 1e6;
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

    // Copy data for temporal structures, this occur just one time
    if(upd == 0){
      data_sp[2].tn = data_sp[0].tn;
      data_sp[2].tf = data_sp[0].tf;
      data_sp[2].r = data_sp[0].r;
      data_sp[2].ma = data_sp[0].ma;

      data_sp[3].tn = data_sp[1].tn;
      data_sp[3].tf = data_sp[1].tf;
      data_sp[3].r = data_sp[1].r;
      data_sp[3].ma = data_sp[1].ma;
    }

    // Check if input data is right
    if((data_sp[0].ch_act + data_sp[1].ch_act + rh + cr) == 0){
      // Return to while for input data
      loop_s = true; 
      Serial.println("Corrupt message - Try again");
    }
  }// End if serial available
}// End function read_data


/**************************************************************/
/******************** Read input data *************************/
/**************************************************************/
void split_functionality(){
  // Execute the rheobase test function
  if(rh && s_c){

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

  } // End if rh separation
  
  if(cr && s_c){
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
  
  // Variables for signal control and reset values to 0 
  unsigned long t_ini_temp = 0;
  unsigned long t_pnfl1 = 0, t_pnfl2 = 0;

  t_stop = 0;

  // Pre-config values for control of state machine both for CH1 and CH2
  /* There is two kind of variable both Ch1 and Ch2 = "x" = 1 = 2
  lpx = loop positive
  lnx = loop negative
  lrx = loop rest
  lfx = loop final
  */
  bool lp1 = 1, ln1 = 1, lr1 = 1, lf1 = 1;
  bool lp2 = 1, ln2 = 1, lr2 = 1, lf2 = 1;

  unsigned int t_pw_2 = int(pw / 2);          // Value for ....

  // Fix PW because time comprobations in while cycle
  pw = pw - t_adc;                    
  
  // Fix PW because time comprobations in while cycle
  bool tn1 = 1;                           // For control loop of CH1
  bool tn2 = 1;                           // For control loop of CH2
  bool B_i = false;                       // For buzzer control
  unsigned long t_tn1 = 0, t_tf1 = 0;     // For time control for CH1
  unsigned long t_tn2 = 0, t_tf2 = 0;     // For time control for CH2

  unsigned long t_ts_temp = 0, t_ts_cal = 0, t_ts_cal_temp = 0; // Control time of time therapy

  unsigned long min_elapsed = 0, Buzzer_Ini = 0;                // Control notification sound

  // Initialize variables
  t_ts_cal = ts * min_t;
  t_stop = micros() + t_ts_cal;
  t_tn1 = micros() + data_sp[0].tn;
  t_tn2 = micros() + data_sp[1].tn;
  t_ts_temp = micros();
  t_ini_temp = t_ts_temp;                 // For update time therapy

  // For sound activation and minutes count
  min_elapsed = min_t + micros();
  int cont_s = 0;                         // Seconds count variable

  // Count minutes time
  //Serial1.println("2>0>");

  // Here occur the magic for therapy stimulation
  while(t_ts_temp < t_stop && s_c){
    // For Tn in Ch1
    if(micros() >= t_tn1 && tn1 && upd == 0 && s_c && ch1){
      tn1 = 0;
      t_tf1 = micros() + data_sp[0].tf;
    }

    // For Tn in Ch2
    if(micros() >= t_tn2 && tn2 && upd == 0 && s_c && ch2){
      tn2 = 0;
      if(data_sp[1].tf > 0){
        t_tf2 = micros() + data_sp[1].tf;
      }
    }
    
    // For Tf in Ch1
    if(micros() >= t_tf1 && tn1 == 0 && upd == 0 && s_c && ch1){
      t_tn1 = micros() + data_sp[0].tn;
      tn1 = 1;
    }
    
    // For Tf in Ch2
    if(micros() >= t_tf2 && tn2 == 0 && upd == 0 && s_c && ch2){
      t_tn2 = micros() + data_sp[1].tn;
      tn2 = 1;
    }
    
    // For positive stimulation in Ch1
    if(micros() <= t_tn1 && lp1 && s_c && upd == 0 && ch1){
      digitalWrite(RELAY_CH_1, 1);
      sendStimValue(0, 1, STIM_ZERO + val_ma(data_sp[0].ma, CH1_MAX_POS));
      lp1 = 0;
      lf1 = 1;
      t_pnfl1 = micros() + pw;
      t_pw_2 = micros() + t_pw_2;
    }

    // For positive stimulation in Ch2
    if(micros() <= t_tn2 && lp2 && s_c && upd == 0 && ch2){
      digitalWrite(RELAY_CH_2, 1);
      sendStimValue(1, 1, STIM_ZERO + val_ma(data_sp[1].ma, CH2_MAX_POS));
      lp2 = 0;
      lf2 = 1;
      t_pnfl2 = micros() + pw;
    }
    
    // For negative stimulation in Ch1
    if(micros() <= t_tn1 && micros() >= t_pnfl1 && lp1 == 0 && ln1 && s_c && upd == 0 && ch1){
      sendStimValue(0, 1, STIM_ZERO - val_ma(data_sp[0].ma, CH1_MIN_NEG));
      ln1 = 0;
      t_pnfl1 = micros() + pw;
    }

    // For negative stimulation in Ch2
    if(micros() <= t_tn2 && micros() >= t_pnfl2 && lp2 == 0 && ln2 && s_c && upd == 0 && ch2){
      sendStimValue(1, 1, STIM_ZERO - val_ma(data_sp[1].ma, CH2_MIN_NEG));
      ln2 = 0;
      t_pnfl2 = micros() + pw;
    }
    
    // For rest stimulation in Ch1
    if(micros() <= t_tn1 && micros() >= t_pnfl1 && ln1 == 0 && lr1 && s_c && upd == 0 && ch1){
      sendStimValue(0, 1, STIM_ZERO);
      lr1 = 0;
      t_pnfl1 = micros() + pw_r;
    }

    // For rest stimulation in Ch2
    if(micros() <= t_tn2 && micros() >= t_pnfl2 && ln2 == 0 && lr2 && s_c && upd == 0 && ch2){
      sendStimValue(1, 1, STIM_ZERO);
      lr2 = 0;
      t_pnfl2 = micros() + pw_r;
    }
    

    // For final rest stimulation in Ch1 and reset variables
    if(micros() <= t_tn1 && micros() >= t_pnfl1 && lr1 == 0 && lf1 && s_c && upd == 0 && ch1){
      lf1 = 0;
      lp1 = 1;
      ln1 = 1;
      lr1 = 1;
    }

    // For final rest stimulation in Ch2 and reset variables
    if(micros() <= t_tn2 && micros() >= t_pnfl2 && lr2 == 0 && lf2 && s_c && upd == 0 && ch2){
      lf2 = 0;
      lp2 = 1;
      ln2 = 1;
      lr2 = 1;
    }
    
    // Verify the time for every minute
    if(micros() >= min_elapsed){
      Serial.println("m");
      cont_s += 1;
      min_elapsed = 60e6 + micros();
      B_i = true;
      digitalWrite(BuzzerPin, 1); // Enable pin buzzer
      Buzzer_Ini = 1e5 + micros();
      Serial1.print("2>");
      Serial1.print(cont_s);
      Serial1.println(">");
    }

    // Activate the buzzer sequence
    if (micros() >= Buzzer_Ini && B_i) {
      digitalWrite(BuzzerPin, 0); // Disable pin buzzer
      B_i = false;
    }

    // Read imput data for update values
    read_dataIn();
    
    // Update values
    if(upd){ 
      sendStimValue(0, 1, STIM_ZERO);
      sendStimValue(1, 1, STIM_ZERO);

      // Update time therapy
      t_ts_cal_temp = ts * min_t;
      if(t_ts_cal != t_ts_cal_temp){
        if(t_ts_cal < t_ts_cal_temp){
          t_stop = t_ini_temp + t_ts_cal_temp;
        } 
        if((t_ts_temp - t_ini_temp) < (t_ini_temp + t_ts_cal_temp)) {
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
        if (lp1 == 0 && ln1 && lf1){
          sendStimValue(0, 1, STIM_ZERO + val_ma(data_sp[0].ma, CH1_MAX_POS));
        } else if (ln1 == 0 && lf1){
          sendStimValue(0, 1, STIM_ZERO - val_ma(data_sp[0].ma, CH1_MIN_NEG));
        }
        data_sp[2].ma = data_sp[0].ma;
      }

      if(data_sp[1].ma != data_sp[3].ma){
        if (lp1 == 0 && ln1 && lf1){
          sendStimValue(1, 1, STIM_ZERO + val_ma(data_sp[1].ma, CH2_MAX_POS));
        } else if (ln1 == 0 && lf1){
          sendStimValue(1, 1, STIM_ZERO - val_ma(data_sp[1].ma, CH2_MIN_NEG));
        }
        data_sp[3].ma = data_sp[1].ma;
      }
      
      upd = 0; // desactivo la actualizacion
    } // Fin update

  t_ts_temp = micros(); // Update micros variable
}// End while update

  // End character for identify finish or stop stimulation
  Serial1.println("3>0>");

  // Bipp for end or stop stimulation
  digitalWrite(BuzzerPin, 1);
  delay(1000);
  digitalWrite(BuzzerPin, 0);
  delay(100);
  digitalWrite(BuzzerPin, 1);
  delay(100);
  digitalWrite(BuzzerPin, 0);


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
}

// For debug
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
/********************* Stop stimulation ************************/
/**************************************************************/
void zeroChannels() {
  digitalWrite(RELAY_CH_1, 0);
  digitalWrite(RELAY_CH_2, 0);
  sendStimValue(0, 1, (uint16_t) (STIM_ZERO + 10));
  sendStimValue(1, 1, (uint16_t) (STIM_ZERO + 10));
}
