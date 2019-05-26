#include <Wire.h>

const int led = 6; 
const int buz = 5;

void setup() 
{
  Wire.begin(0x8);               
  Wire.onReceive(receiveData); 
  pinMode(led, OUTPUT);
  pinMode(buz, OUTPUT);
  digitalWrite(led, LOW); 
  digitalWrite(buz, LOW);
}

void loop() 
{
  
}

void receiveData(int D) 
{
  while (Wire.available()) 
  { 
    char w = Wire.read();
    
    digitalWrite(led, w); 
    digitalWrite(buz, w);
  }
}
