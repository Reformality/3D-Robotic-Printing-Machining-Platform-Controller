float Vo;
float R1 = 100000;
float R2, T, targetT;
float R0 = 100000;
float c1,c2;
int sampleSize = 20;
int sampleRate = 20;
int Vreading;
float sum = 0;
int relay = 31;
//volatile byte relayState = LOW;

void setup() {
  Serial.begin(9600);
  pinMode(relay, OUTPUT);
  digitalWrite(relay, HIGH);
}

void loop() {
  for(int i=0; i < sampleSize; i++)
  {
  Vreading = analogRead(A1);
  sum = sum + Vreading;
  delay(sampleRate);
  }
  Vo = sum/sampleSize;
  sum = 0;

  R2 = R1 * (1023 / (float)Vo - 1.0);
  
  c1 = 1.0/(25.0+273.15);
  c2 = (1.0/3950)*log(R2/R0);
  T = 1.0/(c1+c2);
  T = T - 273.15;

  //Serial.print("Voltage values: "); 
//  Serial.println(Vo); 
  unsigned long timestamp = millis();
  Serial.print(timestamp);
  Serial.print(","); 
  Serial.print(Vo);
  Serial.print(","); 
  Serial.print(R2);
  Serial.print(","); 
  Serial.println(T);
  //Serial.println(" C"); 
  
  // temp control logic
  targetT = 204;

  if(T < targetT) {
    digitalWrite(relay, LOW);
    Serial.println("Closed");
  } 
  else {
    digitalWrite(relay, HIGH);
    Serial.println("Open");
  }
  
//  if(T < 

  
//  if(T<100){
//    digitalWrite(relay, LOW);
//    Serial.println("OFF");
//  } else{
//    digitalWrite(relay, HIGH);
//    Serial.println("ON");
//  }
  
  
  delay(500);
}
