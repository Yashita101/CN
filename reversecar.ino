#include<LiquidCrystal.h>
int buzzer=7;
int led=6;
int trigPin=3;
int echoPin=2;
LiquidCrystal lcd (8,9,4,5,6,7);

void setup() {
  // put your setup code here, to run once:
 lcd.begin(16,2);
 lcd.setCursor(0,0);
 Serial.begin(9600);
 pinMode(buzzer,OUTPUT);
 pinMode(led,OUTPUT);
 pinMode(trigPin,OUTPUT);
 pinMode(echoPin,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
 long duration,inches,cm;
 lcd.setCursor(0,1);
 digitalWrite(trigPin,LOW);
 delayMicroseconds(2);
 digitalWrite(trigPin,HIGH);
 delayMicroseconds(10);
 duration=pulseIn(echoPin,HIGH);
 inches=microsecondsToInches(duration);
 cm=microsecondsToCentimeters(duration);
 if(inches<100)
 {
   Serial.println("close");
  digitalWrite(buzzer,HIGH);
  digitalWrite(led,HIGH);
  
 }
 else
 {
   Serial.println("far");
  digitalWrite(buzzer,LOW);
  digitalWrite(led,LOW);
  
 }
 lcd.print(inches);
 lcd.print("in");
 lcd.print(cm);
 lcd.print("cm");
 Serial.print(inches);
 Serial.println(" in");
 Serial.print(cm);
 Serial.println(" cm");
 delay(1000);
}
long microsecondsToInches(long microseconds)
{
  return microseconds/74/2;
}
long microsecondsToCentimeters(long microseconds)
{
  return microseconds/29/2;
}
