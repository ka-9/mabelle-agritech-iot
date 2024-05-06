// Code generated by Arduino IoT Cloud, DO NOT EDIT.

#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>

const char SSID[]     = SECRET_SSID;    // Network SSID (name)
const char PASS[]     = SECRET_OPTIONAL_PASS;    // Network password (use for WPA, or use as key for WEP)

void onDistanceChange();
void onHumidityChange();
void onNeededNitrogenChange();
void onNeededPhosphorusChange();
void onNeededPotassiumChange();
void onNeededWaterChange();
void onNitrogenChange();
void onPhosphorusChange();
void onPlantedSeedsChange();
void onPotassiumChange();
void onSeedsChange();
void onTemperatureChange();
void onFlagChange();

int distance;
int humidity;
int NeededNitrogen;
int neededPhosphorus;
int neededPotassium;
int neededWater;
int nitrogen;
int phosphorus;
int plantedSeeds;
int potassium;
int seeds;
int temperature;
bool flag;

void initProperties(){

  ArduinoCloud.addProperty(distance, READWRITE, ON_CHANGE, onDistanceChange);
  ArduinoCloud.addProperty(humidity, READWRITE, ON_CHANGE, onHumidityChange);
  ArduinoCloud.addProperty(NeededNitrogen, READWRITE, ON_CHANGE, onNeededNitrogenChange, 0.1);
  ArduinoCloud.addProperty(neededPhosphorus, READWRITE, ON_CHANGE, onNeededPhosphorusChange);
  ArduinoCloud.addProperty(neededPotassium, READWRITE, ON_CHANGE, onNeededPotassiumChange);
  ArduinoCloud.addProperty(neededWater, READWRITE, ON_CHANGE, onNeededWaterChange);
  ArduinoCloud.addProperty(nitrogen, READWRITE, ON_CHANGE, onNitrogenChange);
  ArduinoCloud.addProperty(phosphorus, READWRITE, ON_CHANGE, onPhosphorusChange);
  ArduinoCloud.addProperty(plantedSeeds, READWRITE, ON_CHANGE, onPlantedSeedsChange);
  ArduinoCloud.addProperty(potassium, READWRITE, ON_CHANGE, onPotassiumChange);
  ArduinoCloud.addProperty(seeds, READWRITE, ON_CHANGE, onSeedsChange);
  ArduinoCloud.addProperty(temperature, READWRITE, ON_CHANGE, onTemperatureChange);
  ArduinoCloud.addProperty(flag, READWRITE, ON_CHANGE, onFlagChange);

}

WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);