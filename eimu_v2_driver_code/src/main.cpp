#include <Arduino.h>
#include <SPI.h>
#include "command_functions.h"
#include "vectlab.h"
#include "serial_comm.h"
#include "i2c_comm.h"

float MicroTeslaToTesla(float mT)
{
  return mT * 1000000;
}

unsigned long serialCommTime, serialCommTimeInterval = 5; // ms -> (1000/sampleTime) hz
unsigned long readImuTime, readImuTimeInterval = 20;        // ms -> (1000/sampleTime) hz

void setup()
{
  /* Serial to display data */
  Serial.begin(115200);
  Serial.setTimeout(2);

  //---------------- INITIALIZE IMU -----------------------//
  // start communication with IMU 
  SPI.begin();
  status = imu.begin();
  if (status < 0) {
    Serial.println("IMU initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
    while(1) {}
  }
  //--------------------------------------------------------//

  // loadStoredParams();

  Wire.onReceive(onReceive);
  Wire.onRequest(onRequest);
  Wire.begin(i2cAddress);

  madgwickFilter.setAlgorithmGain(filterGain);
  madgwickFilter.setWorldFrameId(worldFrameId); // 0 - NWU,  1 - ENU,  2 - NED

  pinMode(LED_BUILTIN, OUTPUT);

  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);

  serialCommTime = millis();
  readImuTime = millis();
}

void loop()
{
  // Serial comm loop
  if ((millis() - serialCommTime) >= serialCommTimeInterval)
  {
    recieve_and_send_data();
    serialCommTime = millis();
  }

  if ((millis() - readImuTime) >= readImuTimeInterval)
  {
    imu.readSensor();

    //------------READ SENSOR DATA IN ENU FRAME---------------//
    accRaw[0] = imu.getAccelY_mss();
    accRaw[1] = imu.getAccelX_mss();
    accRaw[2] = -1.00 * imu.getAccelZ_mss();

    gyroRaw[0] = imu.getGyroY_rads();
    gyroRaw[1] = imu.getGyroX_rads();
    gyroRaw[2] = -1.00 * imu.getGyroZ_rads();

    magRaw[0] = imu.getMagY_uT();
    magRaw[1] = imu.getMagX_uT();
    magRaw[2] = -1.00 * imu.getMagZ_uT();
    //--------------------------------------------------------//

    //---------------CALIBRATE SENSOR DATA IN ENU FRAME -----------------//
    // calibrate acc data
    accCal[0] = accRaw[0] - accOff[0];
    accCal[1] = accRaw[1] - accOff[1];
    accCal[2] = accRaw[2] - accOff[2];

    // calibrate gyro data
    gyroCal[0] = gyroRaw[0] - gyroOff[0];
    gyroCal[1] = gyroRaw[1] - gyroOff[1];
    gyroCal[2] = gyroRaw[2] - gyroOff[2];

    // calibrate mag data
    // magCal = A_1*(magRaw - b) using the A matrix and b vector to remove the magnetic offsets
    mag_vect[0] = magRaw[0];
    mag_vect[1] = magRaw[1];
    mag_vect[2] = magRaw[2];

    // mag_vect = mag_vect - b_vect
    mag_vect[0] = mag_vect[0] - magBvect[0];
    mag_vect[1] = mag_vect[1] - magBvect[1];
    mag_vect[2] = mag_vect[2] - magBvect[2];

    // mag_vect = A_mat * mag_vect
    vectOp.transform(mag_vect, magAmat, mag_vect);

    magCal[0] = mag_vect[0];
    magCal[1] = mag_vect[1];
    magCal[2] = mag_vect[2];
    //-----------------------------------------------------//

    //------------- APPLY MADWICK FILTER -----------------//
    float _ax, _ay, _az;
    float _gx, _gy, _gz;
    float _mx, _my, _mz;
    float r, p, y;
    float qw, qx, qy, qz;

    // filter is updated based on the choosen world frame
    switch (worldFrameId)
    {
    case 0: // NWU
      _ax = accCal[1];
      _ay = -1.00 * accCal[0];
      _az = accCal[2];

      _gx = gyroCal[1];
      _gy = -1.00 * gyroCal[0];
      _gz = gyroCal[2];

      _mx = MicroTeslaToTesla(magCal[1]);
      _my = MicroTeslaToTesla(-1.00 * magCal[0]);
      _mz = MicroTeslaToTesla(magCal[2]);
      break;

    case 1: // ENU
      _ax = accCal[0];
      _ay = accCal[1];
      _az = accCal[2];

      _gx = gyroCal[0];
      _gy = gyroCal[1];
      _gz = gyroCal[2];

      _mx = MicroTeslaToTesla(magCal[0]);
      _my = MicroTeslaToTesla(magCal[1]);
      _mz = MicroTeslaToTesla(magCal[2]);
      break;

    case 2: // NED
      _ax = accCal[1];
      _ay = accCal[0];
      _az = -1.00 * accCal[2];

      _gx = gyroCal[1];
      _gy = gyroCal[0];
      _gz = -1.00 * gyroCal[2];

      _mx = MicroTeslaToTesla(magCal[1]);
      _my = MicroTeslaToTesla(magCal[0]);
      _mz = MicroTeslaToTesla(-1.00 * magCal[2]);
      break;
    }
    

    madgwickFilter.madgwickAHRSupdate(_gx, _gy, _gz, _ax, _ay, _az, _mx, _my, _mz);

    madgwickFilter.getOrientationRPY(r, p, y);
    madgwickFilter.getOrientationQuat(qw, qx, qy, qz);

    rpy[0] = r; rpy[1] = p; rpy[2] = y;
    quat[0] = qw; quat[1] = qx; quat[2] = qy; quat[3] = qz;
    //----------------------------------------------------//

    // Serial.println("-----------------------------------");
    // Serial.print("RPY: ");
    // Serial.print(rpy[0], 4); Serial.print("\t");
    // Serial.print(rpy[1], 4); Serial.print("\t");
    // Serial.println(rpy[2], 4);

    // Serial.print("GYR: ");
    // Serial.print(gyroCal[0], 4); Serial.print("\t");
    // Serial.print(gyroCal[1], 4); Serial.print("\t");
    // Serial.println(gyroCal[2], 4);

    // Serial.print("MAG: ");
    // Serial.print(magRaw[0], 4); Serial.print("\t");
    // Serial.print(magRaw[1], 4); Serial.print("\t");
    // Serial.println(magRaw[2], 4);
    // Serial.println("------------------------------------");

    // Serial.println();

    readImuTime = millis();
  }
}