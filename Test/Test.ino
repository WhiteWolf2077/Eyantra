#include <Servo.h>

int analogPin1 = 0;  
int analogPin2 = 2;
int analogPin3 = 4;
int value1 = 0;
int value2 = 0;
int value3 = 0;
int value = 0;
/*Servo stservo;
Servo micservo;
int Buzzer = 13;
*/

void setup()
{
  Serial.begin(9600);
  /*stservo.attach(3);
  micservo.attach(6);
  stservo.write(0);
  micservo.write(0);
 pinMode(Buzzer,OUTPUT);*/
}

/*void servoMotion()
{  
  //Serial.println("");
  micservo.write(60);
  delay(100);
  stservo.write(125);
  delay(100);
  micservo.write(150);
  delay(100);
  stservo.write(0);
  delay(100);

}*/

void lineSenor()
{
  //Serial.print("you you you");
  //digitalWrite(13, HIGH);
  //Serial.println("me me me");
  value1 = analogRead(analogPin1);     // read the input pin
  Serial.print("value1: ");
  Serial.println(value1);
  delay(1000);
  value2 = analogRead(analogPin2);  // read the input pin
  Serial.print("value2: ");
  Serial.println(value2);
  delay(1000);
  value3 = analogRead(analogPin3);  // read the input pin
  Serial.print("value3: ");
  Serial.println(value3);
  delay(1000);
  value = (value1+value2+value3)/3;
 // Serial.println(value);
  if(value1 <=600  && value2 <= 600 && value3 >= 600){
    Serial.write("R");//250,200
    //servoMotion();
   // digitalWrite(Buzzer, HIGH);    
  }
  if(value1 <=600  && value2 >= 600 && value3 >= 600){
    Serial.write("r");//250,220
    //servoMotion();
   // digitalWrite(Buzzer, HIGH);    
  }
  if(value1 <=600  && value2 >= 600 && value3 <= 600){
    Serial.write("F");//250,250
    //servoMotion();
   // digitalWrite(Buzzer, HIGH);    
  }
  if(value1 >=600  && value2 < 600 && value3 < 600){
    Serial.write("L");//200,250
    //servoMotion();
   // digitalWrite(Buzzer, HIGH);    
  }
  if(value1 >=600  && value2 >= 600 && value3 <= 600){
    Serial.write("l");//220,250
    //servoMotion();
   // digitalWrite(Buzzer, HIGH);    
  }
  if(value1 >600  && value2 > 600 && value3 > 600){
    Serial.write("S");
    //servoMotion();
   // digitalWrite(Buzzer, HIGH);    
  }
  
    //servoMotion();
   // digitalWrite(Buzzer, HIGH);    
  
 // else
      //digitalWrite(Buzzer, LOW);    

}

void loop(){
 
      lineSenor();
      delay(100);
//  Serial.println("S");
      
  
}
