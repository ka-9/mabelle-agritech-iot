#include <DHT.h>
// #include <gallery.h> // Uncomment if this is a custom library
#include "thingProperties.h"
#include <SoftwareSerial.h>
#include <Servo.h>
#include <Wire.h>

#define DHTTYPE DHT11
#define DHTPIN 4
#define enA 10
#define enB 11
#define enPump 12
#define in1 A0
#define in2 A1
#define in3 A2
#define in4 A3
#define NPKServo 6
#define plantServo 9

#define RE 8
#define DE 7

// Modbus RTU requests for reading NPK values
const byte nitro[] = {0x01,0x03, 0x00, 0x1e, 0x00, 0x01, 0xe4, 0x0c};
const byte phos[] = {0x01,0x03, 0x00, 0x1f, 0x00, 0x01, 0xb5, 0xcc};
const byte pota[] = {0x01,0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0xc0};

// Declare global variables here
// int nitrogen = 20;
// int phosphorus = 90;
// int potassium = 15;
// int temperature = 34;
// int humidity = 50;
// int seeds = 0;
// int plantedSeeds = 0;
// int distance = 0;
// int neededWater = 0;
// int NeededNitrogen = 0;
// bool flag = false;

int pumpDelay;
Servo plantArm;
Servo NPKArm;

DHT dht(DHTPIN, DHTTYPE);

SoftwareSerial mod(2, 3);
byte values[11];

void setup() {
    Serial.begin(9600);
    pinMode(enA, OUTPUT);
    pinMode(enB, OUTPUT);  
    pinMode(in1, OUTPUT);
    pinMode(in2, OUTPUT);
    pinMode(in3, OUTPUT);
    pinMode(in4, OUTPUT);
    pinMode(enPump, OUTPUT);
    mod.begin(9600);

    // Define pin modes for RE and DE
    pinMode(RE, OUTPUT);
    pinMode(DE, OUTPUT);
     movingDelay = 0;
  
  delay(500);

    plantArm.attach(plantServo);
    NPKArm.attach(NPKServo);
    plantedSeeds = 0;
    dht.begin();  // Initialize the DHT sensor
    initProperties();
    ArduinoCloud.begin(ArduinoIoTPreferredConnection);
    
    setDebugMessageLevel(2);
    ArduinoCloud.printDebugInfo();
}

void loop() {
    ArduinoCloud.update();
    
    byte val1,val2,val3;
   
    humidity = dht.readHumidity();
    temperature = dht.readTemperature();
    Serial.print("Flag: ");
        Serial.println(flag);
  delay(1000);
 
    // Planting logic example
  if(flag){
    
   
    if (plantedSeeds < seeds) {
       movingDelay = (distance/seeds)*100;
       Serial.print("movingDelay: ");
        Serial.println(movingDelay);
        Serial.print("Planted seeds ");
        Serial.println(plantedSeeds);
        if (plantedSeeds % 3 == 0) {
            NPKArm.write(70);
            delay(4000);
            nitrogen = fetchNitrogen();
            delay(250);
            phosphorus = fetchPhosphorous();
            delay(250);
            potassium = fetchPotassium();
            delay(250);
            
            Serial.print(" Nitrogen: ");
            Serial.println(nitrogen);
            Serial.print(" Potassium: ");
            Serial.println(potassium);
            Serial.print(" Phosphorus: ");
            Serial.println(phosphorus);
            // Determine water needs based on neededWater
            switch (neededWater) {
                case 1:
                pumpDelay = 1000;
                break;
                case 2:
                pumpDelay = 1500;
                break;
                case 3:
                pumpDelay = 2000;
                break;
                case 4:
                pumpDelay = 2000;
                break;
                case 5:
                pumpDelay = 3000;
                break;
                default:
                pumpDelay = 500;
            }
        }

        // Not sensing with NPK
        Serial.print("pumpDelay: ");
        Serial.println(pumpDelay);

        plantArm.write(0);
        Serial.println("Planting arm down");
        delay(1000);
        Serial.println("turning pump on");
        pumpOn();
        delay(pumpDelay);
        pumpOff();
        Serial.println("turning pump off");
        Serial.println("Planting arm up");
        delay(1000);
        plantArm.write(90);
        NPKArm.write(0);
        delay(500);
        Serial.println("Moving forward");
        moveFWD(movingDelay);
        brakeMotor();
        plantedSeeds++;
       
      
    } else { // Stop working, planting is done or flag is set to 0

        Serial.println("Planted seeds are done! going back");
        plantedSeeds = 0;
        flag = false;
        delay(10); // Adjust delay based on overall distance
        backward(movingDelay*seeds);
        brakeMotor();
    }
  }else{
   brakeMotor();
   
  }
    
}


void moveFWD(int duration) {
     analogWrite(enA,100);
    analogWrite (enB, 100);
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    delay(duration);
}

void brakeMotor() {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
}

void backward( int duration) {
    analogWrite(enA, 100);
    analogWrite(enB, 100);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    delay(duration);
}

void pumpOn() {
    digitalWrite(enPump, HIGH);
}

void pumpOff() {
    digitalWrite(enPump, LOW);
}

/* Add the onChange functions */
void onCurrentNitrogenChange() {
  // Add your code here to act upon CurrentNitrogen change
}

void onPhosphorusChange() {
  // Add your code here to act upon Phosphorus change
}

void onPotassiumChange() {
  // Add your code here to act upon Potassium change
}

void onNeededNitrogenChange() {
  // Add your code here to act upon NeededNitrogen change
}

void onNeededPotassiumChange() {
  // Add your code here to act upon NeededPotassium change
}

void onNeededPhosphorusChange() {
  // Add your code here to act upon NeededPhosphorus change
}

void onNeededWaterChange() {
  // Add your code here to act upon NeededWater change
}

void onFlagChange() {
  // Add your code here to act upon Flag change
}

void onSeedsChange() {
  // Add your code here to act upon Seeds change
}

void onDistanceChange() {
  // Add your code here to act upon Distance change
}

void onNeededNitrogensChange() {
  // Add your code here to act upon NeededNitrogens change
}

void onPlantedSeedsChange() {
  // Add your code here to act upon PlantedSeeds change
}

void onTemperatureChange() {
  // Add your code here to act upon Temperature change
}

void onHumidityChange() {
  // Add your code here to act upon Humidity change
}

void onNitrogenChange() {
  // Add your code here to act upon Nitrogen change
}

void onShlekChange() {
  // Add your code here to act upon Shlek change
}

void onShrek2Change() {
  // Add your code here to act upon Shrek2 change
}

byte fetchNitrogen(){
  digitalWrite(DE,HIGH);
  digitalWrite(RE,HIGH);
  delay(10);
  if(mod.write(nitro,sizeof(nitro))==8){
    digitalWrite(DE,LOW);
    digitalWrite(RE,LOW);
    for(byte i=0;i<7;i++){
    //Serial.print(mod.read(),HEX);
    values[i] = mod.read();
    Serial.print(values[i],HEX);
    }
    Serial.println();
  }
  return values[4];
}
 
byte fetchPhosphorous(){
  digitalWrite(DE,HIGH);
  digitalWrite(RE,HIGH);
  delay(10);
  if(mod.write(phos,sizeof(phos))==8){
    digitalWrite(DE,LOW);
    digitalWrite(RE,LOW);
    for(byte i=0;i<7;i++){
    //Serial.print(mod.read(),HEX);
    values[i] = mod.read();
    Serial.print(values[i],HEX);
    }
    Serial.println();
  }
  return values[4];
}
 
byte fetchPotassium(){
  digitalWrite(DE,HIGH);
  digitalWrite(RE,HIGH);
  delay(10);
  if(mod.write(pota,sizeof(pota))==8){
    digitalWrite(DE,LOW);
    digitalWrite(RE,LOW);
    for(byte i=0;i<7;i++){
    //Serial.print(mod.read(),HEX);
    values[i] = mod.read();
    Serial.print(values[i],HEX);
    }
    Serial.println();
  }
  return values[4];
}
/*
  Since NeededN is READ_WRITE variable, onNeededNChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onNeededNChange()  {
  // Add your code here to act upon NeededN change
}
/*
  Since NeededP is READ_WRITE variable, onNeededPChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onNeededPChange()  {
  // Add your code here to act upon NeededP change
}
/*
  Since NeededK is READ_WRITE variable, onNeededKChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onNeededKChange()  {
  // Add your code here to act upon NeededK change
}
/*
  Since MovingDelay is READ_WRITE variable, onMovingDelayChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onMovingDelayChange()  {
  // Add your code here to act upon MovingDelay change
}