#ifndef COMMAND_FUNCTIONS_H
#define COMMAND_FUNCTIONS_H

#include <Arduino.h>
#include <Preferences.h>
#include "madgwick_filter.h"
#include "mpu9250_spi.h"
#include <Wire.h>

//--------------- global variables -----------------//
/* Mpu9250 object, SPI bus, CS on pin 5 */
MPU9250 imu(SPI, 5);
int status;

MadgwickFilter madgwickFilter;

float filterGain = 1.0;
int worldFrameId = 1; // 0 - NWU,  1 - ENU,  2 - NED

// initial i2cAddress
uint8_t i2cAddress = 0x68;

// for stored initialization and reset
bool firstLoad = false;
//-------------------------------------------------//Serial.print("GYR: ");

//-------------- IMU MPU6050 ---------------------//
float accOff[3];
float accVar[3];
float accRaw[3];
float accCal[3];

float gyroOff[3];
float gyroVar[3];
float gyroRaw[3];
float gyroCal[3];

float magRaw[3];
float magCal[3];
float magAmat[3][3];
float magBvect[3];
float mag_vect[3];

float rpy[3];
float rpyVar[3];
float quat[4];

//------------------------------------------------//



//--------------- storage variables -----------------//
Preferences storage;

const char * rpyVar_key[3] = {
  "rpyVar0",
  "rpyVar1",
  "rpyVar2",
};

const char * accOff_key[3] = {
  "accOff0",
  "accOff1",
  "accOff2",
};

const char * accVar_key[3] = {
  "accVar0",
  "accVar1",
  "accVar2",
};

const char * gyroOff_key[3] = {
  "gyroOff0",
  "gyroOff1",
  "gyroOff2",
};

const char * gyroVar_key[3] = {
  "gyroVar0",
  "gyroVar1",
  "gyroVar2",
};

const char * magBvect_key[3] = {
  "magBvect0",
  "magBvect1",
  "magBvect2",
};

const char * magAmatR0_key[3] = {
  "magAmatR00",
  "magAmatR01",
  "magAmatR02",
};

const char * magAmatR1_key[3] = {
  "magAmatR10",
  "magAmatR11",
  "magAmatR12",
};

const char * magAmatR2_key[3] = {
  "magAmatR20",
  "magAmatR21",
  "magAmatR22",
};

const char * worldFrameId_key = "worldFrameId";

const char * filterGain_key = "filterGain";

const char * i2cAddress_key = "i2cAddress";

const char * firstLoad_key = "firstLoad";

const char * params_ns = "params"; // preference namespace

void resetParamsInStorage(){
  storage.begin(params_ns, false);

  for (int i=0; i<3; i+=1){
    storage.putFloat(accOff_key[i], 0.0);
    storage.putFloat(accVar_key[i], 0.0);
    storage.putFloat(gyroOff_key[i], 0.0);
    storage.putFloat(gyroVar_key[i], 0.0);
    storage.putFloat(rpyVar_key[i], 0.0);
    storage.putFloat(magBvect_key[i], 0.0);
    storage.putFloat(magAmatR0_key[i], 0.0);
    storage.putFloat(magAmatR1_key[i], 0.0);
    storage.putFloat(magAmatR2_key[i], 0.0);
  }
  storage.putFloat(filterGain_key, 1.0);
  storage.putInt(worldFrameId_key, 1);
  storage.putUChar(i2cAddress_key, 0x68);

  storage.end();
}

void initParams(){
  //check for firstLoad
  storage.begin(params_ns, true);
  firstLoad = storage.getBool(firstLoad_key);
  storage.end();
  // if firsLoad -> reset all params and set firstLoad to false
  if(firstLoad == true){
    resetParamsInStorage();
    firstLoad = false;
    storage.begin(params_ns, false);
    storage.putBool(firstLoad_key, firstLoad);
    storage.end();
  }

}

void loadStoredParams(){
  initParams();
  // load each parameter form the storage to the local variables
  storage.begin(params_ns, true);

  for (int i=0; i<3; i+=1){
    accOff[i] = storage.getFloat(accOff_key[i], 0.0);
    accVar[i] = storage.getFloat(accVar_key[i], 0.0);
    gyroOff[i] = storage.getFloat(gyroOff_key[i], 0.0);
    gyroVar[i] = storage.getFloat(gyroVar_key[i], 0.0);
    rpyVar[i] = storage.getFloat(rpyVar_key[i], 0.0);
    magBvect[i] = storage.getFloat(magBvect_key[i], 0.0);
    magAmat[0][i] = storage.getFloat(magAmatR0_key[i], 0.0);
    magAmat[1][i] = storage.getFloat(magAmatR0_key[i], 0.0);
    magAmat[2][i] = storage.getFloat(magAmatR0_key[i], 0.0);
  }
  filterGain = storage.getFloat(filterGain_key, 1.0);
  worldFrameId = storage.getInt(worldFrameId_key, 1);
  i2cAddress = storage.getUChar(i2cAddress_key, 0x68);

  storage.end();
}


//-------------------------------------------------//




//--------------- global functions ----------------//

String triggerResetParams()
{
  storage.begin(params_ns, false);
  firstLoad = true;
  storage.putBool(firstLoad_key, firstLoad);
  storage.end();
  // reload to reset
  loadStoredParams();
  return "1";
}

// #include "i2c_comm.h"
String setI2cAddress(int address)
{
  if((address <= 0) || (address > 255)){
    return "0";
  }
  else {
    i2cAddress = (uint8_t)address;
    storage.begin(params_ns, false);
    storage.putUChar(i2cAddress_key, i2cAddress);
    storage.end();

    Wire.begin(i2cAddress);

    return "1";
  }  
}
String getI2cAddress()
{
  return String(i2cAddress);
}


String setWorldFrameId(int id)
{
  if((id <= 0) || (id > 2)){
    return "0";
  }
  else {
    worldFrameId = id;
    storage.begin(params_ns, false);
    storage.putInt(worldFrameId_key, worldFrameId);
    storage.end();

    return "1";
  }  
}
String getWorldFrameId()
{
  return String(worldFrameId);
}


String setFilterGain(float gain)
{
  filterGain = gain;
  storage.begin(params_ns, false);
  storage.putFloat(filterGain_key, filterGain);
  storage.end();
  
  return "1"; 
}
String getFilterGain()
{
  return String(filterGain, 3);
}
//-----------------------------------------------------------------//



//------------------------------------------------------------------//
String readRPY(int no)
{
  bool not_allowed = (no < 0) || (no > (2));

  if (not_allowed) 
    return "0.000";

  return String(rpy[no], 6);
}


String readQuat(int no)
{
  bool not_allowed = (no < 0) || (no > (3));

  if (not_allowed) 
    return "0.000";

  return String(quat[no], 6);
}


String readRPYVariance(int no)
{
  bool not_allowed = (no < 0) || (no > (2));

  if (not_allowed) 
    return "0.000";

  return String(rpyVar[no], 8);
}
String writeRPYVariance(int no, float val) {
  bool not_allowed = (no < 0) || (no > (2));

  if (not_allowed) 
    return "0";

  accVar[no] = val;
  storage.begin(params_ns, false);
  storage.putFloat(rpyVar_key[no], rpyVar[no]);
  storage.end();
  return "1";
}


String readAcc(int no)
{
  bool not_allowed = (no < 0) || (no > (2));

  if (not_allowed) 
    return "0.000";

  return String(accCal[no], 6);
}


String readAccRaw(int no)
{
  bool not_allowed = (no < 0) || (no > (2));

  if (not_allowed) 
    return "0.000";

  return String(accRaw[no], 6);
}


String readAccOffset(int no)
{
  bool not_allowed = (no < 0) || (no > (2));

  if (not_allowed) 
    return "0.000";

  return String(accOff[no], 8);
}
String writeAccOffset(int no, float val) {
  bool not_allowed = (no < 0) || (no > (2));
  
  if (not_allowed) 
    return "0";

  accOff[no] = val;
  storage.begin(params_ns, false);
  storage.putFloat(accOff_key[no], accOff[no]);
  storage.end();
  return "1";
}


String readAccVariance(int no)
{
  bool not_allowed = (no < 0) || (no > (2));

  if (not_allowed) 
    return "0.000";

  return String(accVar[no], 8);
}
String writeAccVariance(int no, float val) {
  bool not_allowed = (no < 0) || (no > (2));

  if (not_allowed) 
    return "0";

  accVar[no] = val;
  storage.begin(params_ns, false);
  storage.putFloat(accVar_key[no], accVar[no]);
  storage.end();
  return "1";
}


String readGyro(int no)
{
  bool not_allowed = (no < 0) || (no > (2));

  if (not_allowed) 
    return "0.000";

  return String(gyroCal[no], 6);
}


String readGyroRaw(int no)
{
  bool not_allowed = (no < 0) || (no > (2));

  if (not_allowed) 
    return "0.000";

  return String(gyroRaw[no], 6);
}


String readGyroOffset(int no)
{
  bool not_allowed = (no < 0) || (no > (2));

  if (not_allowed) 
    return "0.000";

  return String(gyroOff[no], 8);
}
String writeGyroOffset(int no, float val) {
  bool not_allowed = (no < 0) || (no > (2));
  
  if (not_allowed) 
    return "0";

  gyroOff[no] = val;
  storage.begin(params_ns, false);
  storage.putFloat(gyroOff_key[no], gyroOff[no]);
  storage.end();
  return "1";
}


String readGyroVariance(int no)
{
  bool not_allowed = (no < 0) || (no > (2));

  if (not_allowed) 
    return "0.000";

  return String(gyroVar[no], 6);
}
String writeGyroVariance(int no, float val) {
  bool not_allowed = (no < 0) || (no > (2));
  
  if (not_allowed) 
    return "0";

  gyroVar[no] = val;
  storage.begin(params_ns, false);
  storage.putFloat(gyroVar_key[no], gyroVar[no]);
  storage.end();
  return "1";
}

String readMag(int no)
{
  bool not_allowed = (no < 0) || (no > (2));

  if (not_allowed) 
    return "0.000";

  return String(magCal[no], 6);
}


String readMagRaw(int no)
{
  bool not_allowed = (no < 0) || (no > (2));

  if (not_allowed) 
    return "0.000";

  return String(magRaw[no], 6);
}


String readMagHardOffset(int no)
{
  bool not_allowed = (no < 0) || (no > (2));

  if (not_allowed) 
    return "0.000";

  return String(magBvect[no], 8);
}
String writeMagHardOffset(int no, float val) {
  bool not_allowed = (no < 0) || (no > (2));
  
  if (not_allowed) 
    return "0";

  magBvect[no] = val;
  storage.begin(params_ns, false);
  storage.putFloat(magBvect_key[no], magBvect[no]);
  storage.end();
  return "1";
}


String readMagSoftOffset0(int no)
{
  bool not_allowed = (no < 0) || (no > (2));

  if (not_allowed) 
    return "0.000";

  return String(magAmat[0][no], 8);
}
String writeMagSoftOffset0(int no, float val) {
  bool not_allowed = (no < 0) || (no > (2));
  
  if (not_allowed) 
    return "0";

  magAmat[0][no] = val;
  storage.begin(params_ns, false);
  storage.putFloat(magAmatR0_key[no], magAmat[0][no]);
  storage.end();
  return "1";
}


String readMagSoftOffset1(int no)
{
  bool not_allowed = (no < 0) || (no > (2));

  if (not_allowed) 
    return "0.000";

  return String(magAmat[1][no], 8);
}
String writeMagSoftOffset1(int no, float val) {
  bool not_allowed = (no < 0) || (no > (2));
  
  if (not_allowed) 
    return "0";

  magAmat[1][no] = val;
  storage.begin(params_ns, false);
  storage.putFloat(magAmatR1_key[no], magAmat[1][no]);
  storage.end();
  return "1";
}


String readMagSoftOffset2(int no)
{
  bool not_allowed = (no < 0) || (no > (2));

  if (not_allowed) 
    return "0.000";

  return String(magAmat[2][no], 8);
}
String writeMagSoftOffset2(int no, float val) {
  bool not_allowed = (no < 0) || (no > (2));
  
  if (not_allowed) 
    return "0";

  magAmat[2][no] = val;
  storage.begin(params_ns, false);
  storage.putFloat(magAmatR2_key[no], magAmat[2][no]);
  storage.end();
  return "1";
}
//-------------------------------------------------------------------//


#endif