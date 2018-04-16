#include <LiquidCrystal.h> //importando biblioteca de LiquidCrustal

LiquidCrystal lcd(8, 13, 9, 4, 5, 6, 7); //config pines en los que se conecta

int key_stado = 0, entrar = 1;

int lcd_key     = 0;       // define os valores representativos de cada botão
int adc_key_in  = 0;
#define btnRIGHT  0
#define btnUP     1
#define btnDOWN   2
#define btnLEFT   3
#define btnSELECT 4
#define btnNONE   5

void setup() {
  Serial.begin(9600);// INICIAMOS EL SERIAL PARA MOSTRAR LOS MENSAJES
  lcd.begin(16, 2);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("   Menu Ppal    ");
  delay(200);
}

void loop() {


  //menu principal
  //while (entrar == 1) {
    lcd_key = read_LCD_buttons();  // Lê os botões
    lcd.setCursor(0, 1);
    lcd.print("TECLA: ");
    lcd.print(lcd_key);
    //delay(200);

    /*    switch (lcd_key)// Para cada botão escolhido, uma ação acontece
        {
          case btnUP:
            {
              lcd.setCursor(0, 1);
              lcd.print("UP");
              break;
            }
          case btnDOWN:
            {
              lcd.setCursor(0, 1);
              lcd.print("DOWN");
              break;
            }
          case btnSELECT:
            {
              lcd.setCursor(0, 1);
              lcd.print("SELECT");
              break;
            }
          case btnLEFT:
            {
              lcd.setCursor(0, 1);
              lcd.print("LEFT");
              break;
            }
          case btnRIGHT:
            {
              lcd.setCursor(0, 1);
              lcd.print("RIGHT");
              break;
            }
        }//fin case

      }//fin while
    */
  }

  //Para capturar los botnes del Keypad de la LCD
int read_LCD_buttons()   // função para ler os valores
  {
    adc_key_in = analogRead(0);
    if (adc_key_in > 1000) {
      return btnNONE;
      lcd.setCursor(0, 1);
      lcd.print("Ninguna        ");
    }

    else if (adc_key_in < 50) {
      return btnRIGHT;
      lcd.setCursor(0, 1);
      lcd.print("Derecha         ");
    }

    else  if (adc_key_in < 250) {
      return btnUP;
      lcd.setCursor(0, 1);
      lcd.print("Arriba          ");
    }

    else if (adc_key_in < 450) {
      return btnDOWN;
      lcd.setCursor(0, 1);
      lcd.print("Abajo           ");
    }

    else  if (adc_key_in < 650) {
      return btnLEFT;
      lcd.setCursor(0, 1);
      lcd.print("Izquierda       ");
    }

    else if (adc_key_in < 850) {
      return btnSELECT;
      lcd.setCursor(0, 1);
      lcd.print("Seleccionar     ");
    }

  }
