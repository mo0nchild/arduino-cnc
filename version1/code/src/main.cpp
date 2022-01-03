#include <Arduino.h>
#include <LiquidCrystal_I2C.h>
#include <GyverEncoder.h>
#include <Stepper_28BYJ_48.h>
#include <Servo.h>
#include <SPI.h>
#include <SD.h>
//#include <MemoryFree.h>
//#include <EEPROM.h>

#define X_STEP 5   
#define Y_STEP 100
#define SERVO_DEG 45
#define SERVO_DELAY 100

#define CLK A2
#define DT A3
#define SW A1

String buffer = "";int bufferPOS = 0;int ENCvalue = -1;int POS_XY[2];
File myFile;File root;bool MISSION_READY = false;byte DIR_SIZE;
String BUFFER = "";String MISSION = "";String FILENAME = "";bool V;

byte CURSOR[8] = {B00000,B01100,B00110,B00011,B00110,B01100,B00000};
byte CURSOR_BACK[8] = {B00000,B00110,B01100,B11000,B11000,B01100,B00110,B00000};

byte S_UPRIGHT[8] = {B00000,B00000,B00000,B10000,B10110,B11110,B01100,B00111};
byte S_UPLEFT[8] = {B00000,B00000,B00000,B00001,B01101,B01111,B00110,B11100};
byte S_DOWNLEFT[8] = {B11100,B00110,B01111,B01101,B00001,B00000,B00000,B00000};
byte S_DOWNRIGHT[8] = {B00111,B01100,B11110,B10110,B10000,B00000,B00000,B00000};

byte T_UPRIGHT[8] = {B00000,B00000,B11000,B01110,B11010,B00010,B01010,B11010};
byte T_UPLEFT[8] = {B00000,B00000,B00011,B01110,B01011,B01000,B01000,B01010};
byte T_DOWNLEFT[8] = {B01011,B01001,B01000,B01111,B00111,B00000,B00000,B00000};
byte T_DOWNRIGHT[8] = {B10010,B00010,B00010,B11110,B11100,B00000,B00000,B00000};

Servo myservo;
Encoder enc(CLK, DT, SW);
LiquidCrystal_I2C lcd(0x27,16,2);

Stepper_28BYJ_48 stepper1(2,3,4,5);
Stepper_28BYJ_48 stepper2(6,7,8,9);

String FILENAME_FUNC(byte UPOS){
  if (!SD.begin(10)) {Serial.println(F("initialization failed!"));return("CAN'T OPEN SD");} 
  else{Serial.println(F("initialization done."));}
  String files = "";DIR_SIZE = 0;byte FILE_POS = 0;byte TRASH = 0;
  root = SD.open("/");while (true) {
    File entry =  root.openNextFile();if(!entry){break;}
    if((String(entry.name()).substring(0,6) != "SYSTEM")&(FILE_POS <= UPOS)){
      files = String(entry.name());FILE_POS++;
    }
    if(String(entry.name()).substring(0,6) == "SYSTEM"){TRASH++;}
    entry.close();DIR_SIZE++;
  }root.close();DIR_SIZE -= TRASH;return files;
}

bool CHECK_CONF(){
  int U = 0;lcd.clear();lcd.setCursor(0,0);lcd.print(F("ARE YOU SURE?"));
  lcd.setCursor(1,1);lcd.print(F("NO"));lcd.setCursor(8,1);lcd.print(F("YES"));
  lcd.setCursor(0,1);lcd.write(byte(1));
  while(true){enc.tick();if(enc.isRightH()){U += 1;if(U > 1){U = 1;}}
    else if(enc.isLeftH()){U -= 1;if(U < 0){U = 0;}}
    if(enc.isPress()){
      if(U == 1){myFile.close();for(int j = 0;j <= 90;j++){myservo.write(j);delay(5);}return(true);}
      else{lcd.clear();lcd.setCursor(0,0);lcd.print(F("PROCESSING..."));
      lcd.setCursor(0,1);lcd.print(F("DON'T REMOVE SD"));return(false);}
    }
    if(enc.isTurn()){
      if(U == 1){lcd.setCursor(0,1);lcd.print(F(" "));lcd.setCursor(7,1);}
      else{lcd.setCursor(7,1);lcd.print(F(" "));lcd.setCursor(0,1);}
      lcd.write(byte(1));
    }
  }
}

void printDIR(){
  /*byte countFILES = 0;
  for(byte i = 0; i < FILES.length();i++){if(FILES.charAt(i) == ' '){countFILES++;}}
  int _FILES[countFILES];byte s = 0;
  for(byte i = 0; i < FILES.length();i++){if(FILES.charAt(i) == ' '){_FILES[s] = i;s++;}}
  for(byte i = 0; i < countFILES; i++){Serial.println(_FILES[i]);}*/

  lcd.clear();lcd.setCursor(0,0);lcd.print(F("CHOOSE FILE:"));bool checker = false;
  lcd.setCursor(1,1);lcd.print(FILENAME_FUNC(0));lcd.setCursor(14,1);lcd.print(F("0"));
  byte U = 1;byte val = 0;byte oldval = 0;String H = FILENAME_FUNC(0);lcd.setCursor(0,1);lcd.write(byte(1));

  while(true){enc.tick();
    if((enc.isRightH())&(U != 0)){val += 1;if(val > DIR_SIZE-1){val = DIR_SIZE-1;}}
    else if((enc.isLeftH())&(U != 0)){val -= 1;if(val == 255){val = 0;}}
    if(enc.isRight()){U += 1;if(U > 1){U = 1;}checker = true;}
    else if(enc.isLeft()){U -= 1;if(U == 255){U = 0;}checker = true;}

    if(enc.isRelease()){checker = false;}
    if((enc.isPress())&(!checker)){if(U != 0){FILENAME = H;MISSION_READY = true;H.remove(H.length());break;}
      else{MISSION_READY = false;H.remove(H.length());break;}}
    if (enc.isTurn()){
        if(U == 1){lcd.setCursor(0,1);lcd.write(byte(1));}
        else{lcd.setCursor(0,1);lcd.write(byte(2));}

        H = FILENAME_FUNC(val);
        if(oldval != val){
        for(byte n = 1; n < 16;n++){lcd.setCursor(n,1);lcd.print(F(" "));}
        lcd.setCursor(1,1);lcd.print(H);oldval = val;lcd.setCursor(14,1);lcd.print(val);}
    }
  }
}

void setupMISSION(){Serial.print(F("Initializing SD card..."));
  if (!SD.begin(10)) {Serial.println(F("initialization failed!"));
    lcd.setCursor(0,0);lcd.print(F("SDCARD NOT INIT"));
    lcd.setCursor(0,1);lcd.print(F("REINSERT&REINIT"));
    while(true){enc.tick();if(enc.isPress()){break;}}return;} 
  else{Serial.println(F("initialization done."));lcd.clear();}

  delay(200);printDIR();delay(200);myFile = SD.open(FILENAME);
  if(MISSION_READY){POS_XY[0] = 0;POS_XY[1] = 0;
  if (myFile) {int j = 0;for(int j = SERVO_DEG;j >= 0;j--){myservo.write(j);delay(10);}
    lcd.clear();lcd.setCursor(0,0);lcd.print(F("PROCESSING..."));
    lcd.setCursor(0,1);lcd.print(F("DON'T REMOVE SD"));

    while (myFile.available()) {
      BUFFER += (char)myFile.read();j++;
      if(BUFFER.length() - 1 >= 0){
        if(BUFFER[BUFFER.length()-1] == ' '){
          MISSION = BUFFER.substring(0,j);int moveTO = 0;int POS = 0;

          if((MISSION.substring(0,1) == String('A'))||(MISSION.substring(0,1) == String('B'))){
            moveTO = MISSION.substring(1,buffer.length()-1).toInt();
            if(moveTO == 0){Serial.println(F("ON "));for(int j = 0;j <= SERVO_DEG;j++){
              enc.tick();if(enc.isPress()){bool CH = CHECK_CONF();if(CH){myFile.close();return;}}myservo.write(j);delay(5);}
            delay(SERVO_DELAY);Serial.println(F("OFF "));for(int j = SERVO_DEG;j >= 0;j--){
              enc.tick();if(enc.isPress()){bool CH = CHECK_CONF();if(CH){myFile.close();return;}}myservo.write(j);delay(5);}delay(SERVO_DELAY);}
            else{
              if (MISSION.substring(0,1) == String('B')){
                Serial.println(F("ON "));for(int j = 0;j <= SERVO_DEG;j++){myservo.write(j);delay(5);
                  enc.tick();if(enc.isPress()){bool CH = CHECK_CONF();if(CH){myFile.close();return;}}}delay(SERVO_DELAY);
              }
              while(POS<moveTO*X_STEP){
                stepper1.step(-1);POS_XY[0]++;POS++;
                //Serial.print(POS);Serial.print("\t");Serial.println(moveTO);
                Serial.print(F("X: "));Serial.print(POS_XY[0]);
                Serial.print(F("\t"));Serial.print(F("Y: "));Serial.println(POS_XY[1]);
                enc.tick();if(enc.isPress()){bool CH = CHECK_CONF();if(CH){myFile.close();return;}}
              }
              if (MISSION.substring(0,1) == String('B')){
                Serial.println(F("OFF "));for(int j = SERVO_DEG;j >= 0;j--){
                  enc.tick();if(enc.isPress()){bool CH = CHECK_CONF();if(CH){myFile.close();return;}}myservo.write(j);delay(5);}
                delay(SERVO_DELAY);
              }
            }
          }

          else if(MISSION.substring(0,1) == String('C')){
            moveTO = MISSION.substring(1,MISSION.length()).toInt();
            //Serial.println("BACK ");Serial.println(moveTO);

            while (POS>moveTO*X_STEP){
              stepper1.step(1);POS_XY[0]--;POS--;
              //Serial.print(POS);Serial.print("\t");Serial.println(moveTO);
              Serial.print(F("X: "));Serial.print(POS_XY[0]);
              Serial.print(F("\t"));Serial.print(F("Y: "));Serial.println(POS_XY[1]);
              enc.tick();if(enc.isPress()){bool CH = CHECK_CONF();if(CH){myFile.close();return;}}
            }
            //Serial.println(F("BACK"));
          }

          else if(MISSION.substring(0,1) == String('-')){
            while(POS < Y_STEP){
              stepper2.step(1);POS++;POS_XY[1]++;Serial.print(F("X: "));Serial.print(POS_XY[0]);
              enc.tick();if(enc.isPress()){bool CH = CHECK_CONF();if(CH){myFile.close();return;}}
              Serial.print(F("\t"));Serial.print(F("Y: "));Serial.println(POS_XY[1]);
            }
          }
          enc.tick();if(enc.isPress()){bool CH = CHECK_CONF();if(CH){myFile.close();return;}}
          moveTO = 0;BUFFER="";j = 0;
        }
      }
    }
    lcd.clear();lcd.setCursor(0,0);lcd.print(F("TASK COMPLETE"));
    myFile.close();delay(2000);
  } else {Serial.println(F("error opening missionFILE"));
    lcd.clear();lcd.setCursor(0,0);lcd.print(F("CAN'T OPEN FILE"));
    while(true){enc.tick();if(enc.isPress()){break;}}}
  } else{myFile.close();return;}
}

void setORIGIN(){lcd.clear();bool checker = false;
  byte U = 1;byte val = 0;byte oldval = 0;byte BUFPOS = 0;
  lcd.setCursor(0,0);lcd.print(F("MOVE ORIGINPOINT"));lcd.setCursor(1,1);lcd.print(F("X:"));
  lcd.setCursor(9,1);lcd.print(F("Y:"));lcd.setCursor(0,1);lcd.write(byte(1));
  lcd.setCursor(4,1);lcd.print(F("5"));lcd.setCursor(12,1);lcd.print(F("5"));

  while(true){enc.tick();
    if((enc.isRightH())&(U != 0)){val += 1;if(val > 1){val = 1;}}
    else if((enc.isLeftH())&(U != 0)){val -= 1;if(val == 255){val = 0;}}
    if(enc.isRight()){U += 1;if(U > 1){U = 1;}checker = true;}
    else if(enc.isLeft()){U -= 1;if(U == 255){U = 0;}checker = true;}

    if(enc.isRelease()){checker = false;}
    if((enc.isPress())&(!checker)){
      if(U != 0){int G = 5;switch(val){
          case 0:
            while (true){enc.tick();
              if(enc.isRightH()){G += 10;if(G > 95){G = 95;}}
              else if(enc.isLeftH()){G -= 10;if(G < -95){G = -95;}}

              if(enc.isPress()){
                if(G*X_STEP>0){int POS = 0;while(POS < G*X_STEP){
                    enc.tick();if(enc.isPress()){break;}stepper1.step(1);POS++;
                  }
                }else{int POS = 0;while(POS > G*X_STEP){
                    enc.tick();if(enc.isPress()){break;}stepper1.step(-1);POS--;
                  }
                }break;
              }
              if(enc.isTurn()){
                for(byte i = 3;i < 6;i++){lcd.setCursor(i,1);lcd.print(F(" "));}
                if(G < 0){lcd.setCursor(3,1);}
                else{lcd.setCursor(4,1);}
                lcd.print(G);
              }
            }
            for(byte i = 3;i < 6;i++){lcd.setCursor(i,1);lcd.print(F(" "));}
            lcd.setCursor(4,1);lcd.print(F("5"));
            break;
          case 1:
            while (true){enc.tick();
              if(enc.isRightH()){G += 10;if(G > 95){G = 95;}}
              else if(enc.isLeftH()){G -= 10;if(G < -95){G = -95;}}

              if(enc.isPress()){
                if(G*Y_STEP>0){int POS = 0;while(POS < G*Y_STEP){stepper2.step(1);
                    enc.tick();if(enc.isPress()){break;}POS++;
                  }
                }else{int POS = 0;while(POS > G*Y_STEP){stepper2.step(-1);
                    enc.tick();if(enc.isPress()){break;}POS--;
                  }
                }break;
              }
              if(enc.isTurn()){
                for(byte i = 11;i < 14;i++){
                  lcd.setCursor(i,1);lcd.print(F(" "));
                }
                if(G < 0){lcd.setCursor(11,1);}
                else{lcd.setCursor(12,1);}
                lcd.print(G);
              }
            }
            for(byte i = 11;i < 14;i++){lcd.setCursor(i,1);lcd.print(F(" "));}
            lcd.setCursor(12,1);lcd.print(F("5"));
            break;
          default:break;
          //lcd.clear();lcd.setCursor(0,0);lcd.print(F("MOVE ORIGIN PT"));lcd.setCursor(1,1);lcd.print(F("X:"));
          //lcd.setCursor(9,1);lcd.print(F("Y:"));lcd.setCursor(BUFPOS,1);lcd.write(byte(1));
        }
      }
      else{return;}}
    if(enc.isTurn()){
        if(U == 1){lcd.setCursor(BUFPOS,1);lcd.write(byte(1));}
        else{lcd.setCursor(BUFPOS,1);lcd.write(byte(2));}
        if(oldval != val){
          if(val == 0){BUFPOS = 0;lcd.setCursor(8,1);lcd.print(" ");}
          else{BUFPOS = 8;lcd.setCursor(0,1);lcd.print(" ");}
          lcd.setCursor(BUFPOS,1);lcd.write(byte(1));oldval = val;
        }
    }
  }
}

void settingsMENU(){lcd.clear();bool checker = false;
  byte U = 1;byte val = 0;byte oldval = 0;lcd.setCursor(0,0);lcd.write(byte(1));
  lcd.setCursor(1,0);lcd.print(F("SET VALUE"));lcd.setCursor(1,1);lcd.print(F("SET ORIGIN"));

  while(true){enc.tick();
    if((enc.isRightH())&(U != 0)){val += 1;if(val > 1){val = 1;}}
    else if((enc.isLeftH())&(U != 0)){val -= 1;if(val == 255){val = 0;}}

    if(enc.isRight()){U += 1;if(U > 1){U = 1;}checker = true;}
    else if(enc.isLeft()){U -= 1;if(U == 255){U = 0;}checker = true;}

    if(enc.isRelease()){checker = false;}
    if((enc.isPress())&(!checker)){
      if(U != 0){switch(val){
          case 0:
            for(int j = 0;j <= SERVO_DEG;j++){myservo.write(j);delay(10);}
            for(int j = SERVO_DEG;j >= 0;j--){myservo.write(j);delay(10);}
            break;
          case 1:setORIGIN();break;
          default:break;}
          lcd.clear();lcd.setCursor(0,val);lcd.write(byte(1));
          lcd.setCursor(1,0);lcd.print(F("SET VALUE"));lcd.setCursor(1,1);lcd.print(F("SET ORIGIN"));
      }
      else{return;}}
    if (enc.isTurn()){
        if(U == 1){lcd.setCursor(0,val);lcd.write(byte(1));}
        else{lcd.setCursor(0,val);lcd.write(byte(2));}
        if(oldval != val){lcd.setCursor(0,oldval);lcd.print(F(" "));
          lcd.setCursor(0,val);lcd.write(byte(1));oldval = val;
        }
    }
  }
}

void RESET_MAINMENU(byte VALUE){lcd.clear();
  lcd.createChar(1, CURSOR);lcd.createChar(2, CURSOR_BACK);
  lcd.createChar(3, T_UPLEFT);lcd.createChar(4, T_UPRIGHT);
  lcd.createChar(5, T_DOWNLEFT);lcd.createChar(6, T_DOWNRIGHT);

  if(VALUE != 1){
    lcd.setCursor(0,1);lcd.print(F(" "));
    lcd.createChar(3, T_UPLEFT);lcd.createChar(4, T_UPRIGHT);
    lcd.createChar(5, T_DOWNLEFT);lcd.createChar(6, T_DOWNRIGHT);
  }
  else{
    lcd.setCursor(0,0);lcd.print(F(" "));
    lcd.createChar(3, S_UPLEFT);lcd.createChar(4, S_UPRIGHT);
    lcd.createChar(5, S_DOWNLEFT);lcd.createChar(6, S_DOWNRIGHT);
  }

  lcd.setCursor(0,VALUE);lcd.write(byte(1));
  lcd.setCursor(12,0);lcd.write(byte(3));lcd.setCursor(13,0);lcd.write(byte(4));
  lcd.setCursor(12,1);lcd.write(byte(5));lcd.setCursor(13,1);lcd.write(byte(6));
  lcd.setCursor(1,0);lcd.print(F("START TASK"));
  lcd.setCursor(1,1);lcd.print(F("SETTINGS"));
}

void setup() {Serial.begin(9600);enc.setType(TYPE2);myservo.attach(14);myservo.write(0);
  lcd.init();lcd.backlight();lcd.clear();pinMode(10, OUTPUT);
  char S1[14] = "_ARDUINO_CNC_"; char S2[10] = "_PLOTTER_";int b = 0;

  for(int i = 1;i < 15; i++){
    if(i == 1){lcd.setCursor(i,0);lcd.write(255);}
    else{lcd.setCursor(i-1,0);lcd.write(S1[b]);lcd.setCursor(i,0);lcd.write(255);b++;}
  delay(50);}b = 0;lcd.setCursor(14,0);lcd.print(" ");

  for(int i = 2;i < 12; i++){
    if(i == 2){lcd.setCursor(i,1);lcd.write(255);}
    else{lcd.setCursor(i-1,1);lcd.write(S2[b]);lcd.setCursor(i,1);lcd.write(255);b++;}
  delay(50);}b = 0;

  while(b<4){lcd.setCursor(11,1);lcd.print(" ");delay(200);
    lcd.setCursor(11,1);lcd.write(255);delay(500);b++;}
  RESET_MAINMENU(0);
}

void loop() {enc.tick();
  if (enc.isRightH()){ENCvalue += 1;if(ENCvalue > 1){ENCvalue = 1;}}   
  if (enc.isLeftH()){ENCvalue -= 1;if(ENCvalue < 0){ENCvalue = 0;}}
  
  if (enc.isPress()){switch(ENCvalue){
      case -1:ENCvalue = 0;V = false;break;
      case 0:setupMISSION();
        if(MISSION_READY){lcd.clear();lcd.setCursor(0,0);lcd.print(F("MOVE TO ORIGIN"));
        lcd.setCursor(0,1);lcd.print(F("PLEASE WAIT..."));
        for(int j = SERVO_DEG;j >= 0;j--){myservo.write(j);delay(10);}
        bool J = false;int POS = 0;while(POS > -POS_XY[0]*X_STEP){
          enc.tick();if(enc.isPress()){J = true;break;}stepper1.step(1);POS--;
        }
        POS = 0;while(POS > -POS_XY[1]*Y_STEP){
          enc.tick();if((enc.isPress())||(J)){break;}stepper2.step(-1);POS--;
        }
        POS_XY[0] = 0;POS_XY[1] = 0;delay(1000);MISSION_READY = false;}break;
      case 1:settingsMENU();break;
      default:break;}
      if(V){delay(200);RESET_MAINMENU(ENCvalue);}else{V = true;}
  }
  
  if (enc.isTurn()) {
    if(ENCvalue != 1){
      lcd.setCursor(0,1);lcd.print(F(" "));
      lcd.createChar(3, T_UPLEFT);lcd.createChar(4, T_UPRIGHT);
      lcd.createChar(5, T_DOWNLEFT);lcd.createChar(6, T_DOWNRIGHT);
    }
    else{
      lcd.setCursor(0,0);lcd.print(F(" "));
      lcd.createChar(3, S_UPLEFT);lcd.createChar(4, S_UPRIGHT);
      lcd.createChar(5, S_DOWNLEFT);lcd.createChar(6, S_DOWNRIGHT);
    }
    lcd.setCursor(0,ENCvalue);lcd.write(byte(1));
    lcd.setCursor(12,0);lcd.write(byte(3));lcd.setCursor(13,0);lcd.write(byte(4));
    lcd.setCursor(12,1);lcd.write(byte(5));lcd.setCursor(13,1);lcd.write(byte(6));
  }
  
}