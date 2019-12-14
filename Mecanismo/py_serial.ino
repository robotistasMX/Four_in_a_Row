int pl[] = {10, 9, 8, 7, 6, 5, 4};

void off() {
  for (int i = 10; i >= 4; i--)
    digitalWrite(i, LOW);
}

void setup() {
  Serial.begin(9600);
  for (int i = 10; i >= 4; i--)
    pinMode(i, OUTPUT);
  off();
}


bool b=0;

void loop() {
  if (Serial.available() > 0) {
    int k = Serial.read()- '0';
      if(k==8){
        for (int i = 0; i <= 6; i++) {
          digitalWrite(pl[i], HIGH);
          delay(50);
        }
        off();
        for (int i = 6; i >= 0; i--) {
          digitalWrite(pl[i], HIGH);
          delay(50);
        }
        b=1;
       }
       else
        b=0;
    off();
    digitalWrite(pl[k], HIGH);
    delay(6000);
    off();
  }
  else {
    off();
    if(b==1){
      for (int i = 0; i <= 6; i++) {
          digitalWrite(pl[i], HIGH);
          delay(50);
        }
        off();
        for (int i = 6; i >= 0; i--) {
          digitalWrite(pl[i], HIGH);
          delay(50);
        }
    }
    off();
  }
  Serial.flush();
  delay(30);
}
