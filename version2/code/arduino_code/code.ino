#include <AccelStepper.h>
#include <EEPROM.h>
#include <Servo.h>
#define DIR1 2
#define STEP1 3
#define MAXSPEED1 400
#define ACCEL1 400

#define DIR2 4 
#define STEP2 5
#define MAXSPEED2 400
#define ACCEL2  400

#define SERVO_PIN 9
#define INTERFACE_TYPE 1
#define X_STEP_PIXEL 10
#define Y_STEP_PIXEL 12

AccelStepper stepper1 = AccelStepper(INTERFACE_TYPE, STEP1, DIR1);
AccelStepper stepper2 = AccelStepper(INTERFACE_TYPE, STEP2, DIR2);
String DATA = "";int X = 0; int Y = 0;Servo myservo;
bool servo_pos = false;

int STEPS_COUNT(String TEXT){
  return String(TEXT.substring(1,TEXT.length())).toInt();
}

void AXIS_MOVE(String move_data){
  String task = move_data.substring(0,1) + String(STEPS_COUNT(move_data));
  Serial.println(task);
  stepper2.setMaxSpeed(MAXSPEED2);stepper2.setAcceleration(ACCEL2);
  stepper1.setMaxSpeed(MAXSPEED1);stepper1.setAcceleration(ACCEL1);
  if(move_data.substring(0,1) == "X"){
    X += STEPS_COUNT(move_data);stepper1.moveTo(X*X_STEP_PIXEL);
    stepper1.runToPosition();
  }
  else if(move_data.substring(0,1) == "Y"){
    Y += STEPS_COUNT(move_data);stepper2.moveTo(Y*Y_STEP_PIXEL);
    stepper2.runToPosition();
  }
  else if(move_data.substring(0,1) == "M"){
    stepper1.moveTo(0);stepper1.runToPosition();stepper2.moveTo(0);stepper2.runToPosition();
    tone(14, 600);delay(200);tone(14, 900);delay(500);noTone(14);
  }
  Serial.println("ACCEPT");
}

void USING_DEVICE(String device_data){
  Serial.println(device_data);int pos = 0;
  if((STEPS_COUNT(device_data) == 1)&(servo_pos == false)){
    for(pos = 0; pos <= 30; pos += 1){myservo.write(pos);delay(10);}
    servo_pos = true;
  }else if((STEPS_COUNT(device_data) == 0)&(servo_pos != false)){
    for(pos = 30; pos >= 0; pos -= 1) {myservo.write(pos);delay(10);}
    servo_pos = false;  
  }Serial.println("ACCEPT");
}

void SET_SETTINGS(String settings_data){
  Serial.println(settings_data);Serial.println("ACCEPT");
}

void SET_ORIGIN(String set_data){
  Serial.println(set_data);X = 0;Y = 0;
  stepper1.setCurrentPosition(0);stepper2.setCurrentPosition(0);Serial.println("ACCEPT");
}
void setup() {Serial.begin(115200);pinMode(14, OUTPUT);myservo.attach(SERVO_PIN);myservo.write(0);}

void loop() {char inByte;
  if (Serial.available() > 0) {
    inByte = Serial.read();
    //Serial.println(inByte);
    if(inByte == ' '){
      String TASK_TYPE = DATA.substring(0,1);
      if((TASK_TYPE == "X")||(TASK_TYPE == "Y")||(TASK_TYPE == "M")){AXIS_MOVE(DATA);}
      else if(DATA.substring(0,1) == "D"){USING_DEVICE(DATA);}
      else if(DATA.substring(0,1) == "S"){SET_SETTINGS(DATA);}
      else if(DATA.substring(0,1) == "R"){SET_ORIGIN(DATA);}
      DATA = "";
    }
    else{DATA += inByte;}
    delay(5);
  }
}
