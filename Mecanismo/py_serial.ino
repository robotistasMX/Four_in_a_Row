void off(){ 
   digitalWrite(13, LOW);
   digitalWrite(12, LOW);
   digitalWrite(11, LOW);
   digitalWrite(10, LOW);
   digitalWrite(9, LOW);
   digitalWrite(8, LOW);
   digitalWrite(7, LOW);
}
void setup()
{
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(7, OUTPUT);

  off();

  Serial.begin(9600);
}

void loop()
{
  
  if (Serial.available() > 0)
  {
    int k=Serial.read();
    if (k == '0')
    {
      off();
      digitalWrite(13, HIGH);
    }
    else if (k == '1')
    {
      off();
      digitalWrite(12, HIGH);
    }
    else if (k == '2')
    {
      off();
      digitalWrite(11, HIGH);
    }
    else if (k == '3')
    {
      off();
      digitalWrite(10, HIGH);
    }
    else if (k == '4')
    {
      off();
      digitalWrite(9, HIGH);
    }
    else if (k == '5')
    {
      off();
      digitalWrite(8, HIGH);
    }
    else if (k == '6')
    {
      off();
      digitalWrite(7, HIGH);
    }
  }
  Serial.flush();
  delay(30);

}
