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

    /**************** Importante para tener por lo menos 1s antes de estimular y poder capturar datos *****************/
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