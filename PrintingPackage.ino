#include <Stepper.h>

//control extruder, bed, fan, feeding stepper


//Extruder
float targetTE = 220.0; 
float TE;
//Bed
float targetTBed = 60.0; 
float TB;

//stepper
// Number of steps per output rotation
const int stepsPerRevolution = 200;
// Create Instance of Stepper library
Stepper myStepper(stepsPerRevolution, 31, 33, 35, 37);

//Define pins
const int ThermistorE = A0;
const int ThermistorB = A2;
const int relayExtruder = 22;
const int relayBed = 24;
const int heatingStart = 52; //receive signal from dorna to start heating
const int printStart = 53; //receive signal from dorna to start feeding filament
const int tempReady = 50;

//other var
bool tempReadyState = false;





void setup() {
  Serial.begin(9600);
  pinMode(relayExtruder, OUTPUT);
  digitalWrite(relayExtruder, HIGH);
  pinMode(relayBed, OUTPUT);
  digitalWrite(relayBed, HIGH);
  myStepper.setSpeed(4);
  pinMode(heatingStart, INPUT);
  pinMode(printStart, INPUT);
  pinMode(tempReady, OUTPUT);
  digitalWrite(tempReady, LOW);
  tempReadyState = false;
}

void loop() {
  Serial.print("heatingStart:");
  Serial.println(digitalRead(heatingStart));
  Serial.print("printStart:");
  Serial.println(digitalRead(printStart));
  Serial.print("tempReady:");
  // Serial.println(digitalRead(tempReady));
  Serial.println(tempReadyState)
  
  if(digitalRead(heatingStart) == 1 || digitalRead(printStart) == 1){
    TE = heatingOF(targetTE, ThermistorE, relayExtruder);
    Serial.print("Extruder_temperature:");
    Serial.println(TE);
    TB = heatingOF(targetTBed, ThermistorB, relayBed);
    Serial.print("Bed_temperature:");
    Serial.println(TB);
  }else
  {
    digitalWrite(relayExtruder, HIGH);
    digitalWrite(relayBed, HIGH);
  }
  
  if(((TE>(targetTE-10) && TB>(targetTBed-5) )||tempReadyState)&&(digitalRead(heatingStart) == 1 || digitalRead(printStart) == 1)){// && TB>55
    digitalWrite(tempReady,HIGH);
  }
  else if(digitalRead(heatingStart) == 0 && digitalRead(printStart) == 0){
    digitalWrite(tempReady,LOW);
  }
  else{
    digitalWrite(tempReady,LOW);
  }
//  
  if(digitalRead(printStart) == 1){
    myStepper.step(1);
    Serial.println("feeding started");
    }
  

  //delay(500);
}

float heatingOF(int targetT, int Thermistor, int relay){
  //Thermistor common constant
  float R0 = 100000;
  float R1 = 100000;
  float c1,c2;
  float sum = 0;
  int sampleSize = 20;
  int sampleRate = 0;
  //
  float Vo;
  int Vreading;
  float R2, T;
  //
  int state = 1;

  //Extruder
  //read in analoge voltage
  for(int i=0; i < sampleSize; i++)
  {
  Vreading = analogRead(Thermistor);
  sum = sum + Vreading;
  delay(sampleRate);
  }
  Vo = sum/sampleSize;
  sum = 0;
  
  //Calculate thermistor resistance based on averaged voltage
  R2 = R1 * (1023 / (float)Vo - 1.0);
  
  //Calculate temperature based on resistance
  c1 = 1.0/(25.0+273.15);
  c2 = (1.0/3950)*log(R2/R0);
  T = 1.0/(c1+c2);
  T = T - 273.15;
  
  // temp control logic
  if(T < (targetT+5)) {
    digitalWrite(relay, LOW);
    state = 0; //closed
    Serial.print("Relay state:");
    Serial.println(state);
  } 
  else {
    digitalWrite(relay, HIGH);
    state = 1; //open
    Serial.print("Relay state:");
    Serial.println(state);
  }
  
  
  //print data
  unsigned long timestamp = millis();
//  Serial.print(timestamp);
//  Serial.print(","); 
//  Serial.print(","); 
//  Serial.print(Vo);
//  Serial.print(","); 
  Serial.print(R2);
  Serial.print(","); 

  return T;
}