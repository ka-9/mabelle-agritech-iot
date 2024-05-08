#include <DHT.h>
// #include <gallery.h> // Uncomment if this is a custom library
#include "thingProperties.h"
#include <SoftwareSerial.h>
#include <Servo.h>

#define DHTTYPE DHT11
#define DHTPIN 4
#define en 5
#define in1 A0
#define in2 A1
#define in3 A2
#define in4 A3
#define NPKServo 6
#define plantServo 9

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
    pinMode(en, OUTPUT);
    pinMode(in1, OUTPUT);
    pinMode(in2, OUTPUT);
    pinMode(in3, OUTPUT);
    pinMode(in4, OUTPUT);

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

    humidity = dht.readHumidity();
    temperature = dht.readTemperature();
    Serial.print("Flag: ");
        Serial.println(flag);

  
  
    // Planting logic example
    if (flag && plantedSeeds < seeds) {
        Serial.print("Planted seeds ");
        Serial.println(plantedSeeds);
        if (plantedSeeds % 3 == 0) {
            NPKArm.write(70);
            delay(4000);
            nitrogen = random(0, 110);
            potassium = random(0, 25);
            phosphorus = random(0, 32);
            Serial.print(" Nitrogen: ");
            Serial.println(nitrogen);
            Serial.print(" Potassium: ");
            Serial.println(potassium);
            Serial.print(" Phosphorus: ");
            Serial.println(phosphorus);
            // Determine water needs based on neededWater
            switch (neededWater) {
                case 1:
                pumpDelay = 100;
                break;
                case 2:
                pumpDelay = 200;
                break;
                case 3:
                pumpDelay = 300;
                break;
                case 4:
                pumpDelay = 400;
                break;
                case 5:
                pumpDelay = 500;
                break;
                default:
                pumpDelay = 0;
            }
        }

        // Not sensing with NPK
        Serial.print("pumpDelay: ");
        Serial.println(pumpDelay);

        plantArm.write(70);
        Serial.println("Planting arm down");
        Serial.println("turning pump on");
        pumpOn();
        delay(pumpDelay);
        pumpOff();
        Serial.println("turning pump off");
        Serial.println("Planting arm up");
        plantArm.write(0);
        NPKArm.write(0);
        moveFWD();
        delay(10); // Adjust delay according to movement speed
        plantedSeeds++;
        brakeMotor();
      
    } else { // Stop working, planting is done or flag is set to 0

        Serial.println("Planted seeds are done! going back");
        plantedSeeds = 0;
        flag = false;
        backward();
        delay(10); // Adjust delay based on overall distance
        brakeMotor();
    }
    
}


void moveFWD() {
    analogWrite(en, 255);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
}

void brakeMotor() {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
}

void backward() {
    analogWrite(en, 255);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
}

void pumpOn() {
  // Implement logic to activate the pump
}

void pumpOff() {
  // Implement logic to deactivate the pump
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