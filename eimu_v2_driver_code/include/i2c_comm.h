#ifndef I2C_COMM_H
#define I2C_COMM_H

#include <Wire.h>
#include "command_functions.h"

String i2cDataMsg = "", i2cDataMsgBuffer = "", i2cDataMsgBufferArray[3];
String i2cSendMsg = "";


void onRequest() {
  char charArray[i2cSendMsg.length() + 1];
  i2cSendMsg.toCharArray(charArray, i2cSendMsg.length() + 1);
  Wire.slaveWrite((u_int8_t *)charArray, i2cSendMsg.length());

  i2cSendMsg = "";
}


void onReceive(int dataSizeInBytes) {
  int indexPos = 0, i = 0;

  for (int i = 0; i < dataSizeInBytes; i += 1)
  {
    char c = Wire.read();
    i2cDataMsg += c;
  }

  i2cDataMsg.trim();

  if (i2cDataMsg != "")
  {
    do
    {
      indexPos = i2cDataMsg.indexOf(',');
      if (indexPos != -1)
      {
        i2cDataMsgBuffer = i2cDataMsg.substring(0, indexPos);
        i2cDataMsg = i2cDataMsg.substring(indexPos + 1, i2cDataMsg.length());
        i2cDataMsgBufferArray[i] = i2cDataMsgBuffer;
        i2cDataMsgBuffer = "";
      }
      else
      {
        if (i2cDataMsg.length() > 0)
          i2cDataMsgBufferArray[i] = i2cDataMsg;
      }
      i += 1;
    } while (indexPos >= 0);
  }

  if (i2cDataMsgBufferArray[0] != "")
  {
    int pos = i2cDataMsgBufferArray[1].toInt();
    bool pos_not_found = (pos < 0) || (pos > (3));

    digitalWrite(LED_BUILTIN, HIGH);

    if (i2cDataMsgBufferArray[0] == "/rpy")
    {
      if (pos_not_found)
        i2cSendMsg = "0.00";
      else
        i2cSendMsg = readRPY(pos);
      Serial.println(i2cSendMsg);
    }

    if (i2cDataMsgBufferArray[0] == "/quat")
    {
      if (pos_not_found)
        i2cSendMsg = "0.00";
      else
        i2cSendMsg = readQuat(pos);
    }

    else if (i2cDataMsgBufferArray[0] == "/rpy-var")
    {
      if (i2cDataMsgBufferArray[2] == ""){
        if (pos_not_found)
          i2cSendMsg = "0.00";
        else
          i2cSendMsg = readRPYVariance(pos);
      }
      else {
        if (pos_not_found)
          i2cSendMsg = "0";
        else
          i2cSendMsg = writeRPYVariance(pos, i2cDataMsgBufferArray[2].toFloat());
      }
    }

    if (i2cDataMsgBufferArray[0] == "/acc")
    {
      if (pos_not_found)
        i2cSendMsg = "0.00";
      else
        i2cSendMsg = readAcc(pos);
    }

    else if (i2cDataMsgBufferArray[0] == "/acc-var")
    {
      if (i2cDataMsgBufferArray[2] == ""){
        if (pos_not_found)
          i2cSendMsg = "0.00";
        else
          i2cSendMsg = readAccVariance(pos);
      }
      else {
        if (pos_not_found)
          i2cSendMsg = "0";
        else
          i2cSendMsg = writeAccVariance(pos, i2cDataMsgBufferArray[2].toFloat());
      }
    }

    else if (i2cDataMsgBufferArray[0] == "/gyro")
    {
      if (pos_not_found)
        i2cSendMsg = "0.00";
      else
        i2cSendMsg = readGyro(pos);
    }

    else if (i2cDataMsgBufferArray[0] == "/gyro-var")
    {
      if (i2cDataMsgBufferArray[2] == ""){
        if (pos_not_found)
          i2cSendMsg = "0.00";
        else
          i2cSendMsg = readGyroVariance(pos);
      }
      else {
        if (pos_not_found)
          i2cSendMsg = "0";
        else
          i2cSendMsg = writeGyroVariance(pos, i2cDataMsgBufferArray[2].toFloat());
      }
    }

    if (i2cDataMsgBufferArray[0] == "/mag")
    {
      if (pos_not_found)
        i2cSendMsg = "0.00";
      else
        i2cSendMsg = readMag(pos);
    }

    else if (i2cDataMsgBufferArray[0] == "/gain")
    {
      i2cSendMsg = getFilterGain();
    }

    else if (i2cDataMsgBufferArray[0] == "/frame-id")
    {
      if (i2cDataMsgBufferArray[2] == ""){
        i2cSendMsg = getWorldFrameId();
      }
      else {
        i2cSendMsg = setWorldFrameId(i2cDataMsgBufferArray[2].toInt());
      }
    }


    digitalWrite(LED_BUILTIN, LOW);
  }
  else
  {
    digitalWrite(LED_BUILTIN, HIGH);

    i2cSendMsg = "0";

    digitalWrite(LED_BUILTIN, LOW);
  }

  i2cDataMsg = "";
  i2cDataMsgBuffer = "";
  i2cDataMsgBufferArray[0] = "";
  i2cDataMsgBufferArray[1] = "";
  i2cDataMsgBufferArray[2] = "";
}

#endif