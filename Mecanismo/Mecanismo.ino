#include <Servo.h>
Servo myservo;
const int pw[]={0,5,6}; //Pines de los motores
const int rg[]={0,7,4};
const int lf[]={0,8,9};

void setup(){
  myservo.attach(3);
  for(int i=1; i<=2; i++){
    pinMode(pw[i],OUTPUT);
    pinMode(rg[i],OUTPUT);
    pinMode(lf[i],OUTPUT);
  }
  Serial.begin(9600); // Starts the serial communication
}

void loop(){
  /*analogWrite(pw[1],80);
  digitalWrite(rg[1],1);
  digitalWrite(lf[1],0);
  delay(200);
  digitalWrite(rg[1],0);
  while(true);*/
  for (pos = 80; pos <= 180; pos += 2) {
    myservo.write(pos);
    delay(15);
  }
  for (pos = 180; pos >= 80; pos -= 4) {
    myservo.write(pos);
    delay(15);
  }
  delay(1000);
}
