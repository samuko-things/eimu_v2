#ifndef SERIAL_COMM_H
#define SERIAL_COMM_H

#include "command_functions.h"

String dataMsg = "", dataMsgBuffer = "", dataMsgBufferArray[3];
String sendMsg = "";


void recieve_and_send_data(){
  int indexPos = 0, i = 0;

  if (Serial.available() > 0)
  {
    while (Serial.available())
    {
      dataMsg = Serial.readString();
    }
    dataMsg.trim();
    if (dataMsg != "")
    {
      do
      {
        indexPos = dataMsg.indexOf(',');
        if (indexPos != -1)
        {
          dataMsgBuffer = dataMsg.substring(0, indexPos);
          dataMsg = dataMsg.substring(indexPos + 1, dataMsg.length());
          dataMsgBufferArray[i] = dataMsgBuffer;
          dataMsgBuffer = "";
        }
        else
        {
          if (dataMsg.length() > 0)
            dataMsgBufferArray[i] = dataMsg;
        }
        i += 1;
      } while (indexPos >= 0);
    }


    if (dataMsgBufferArray[0] != "")
    {
      int pos = dataMsgBufferArray[1].toInt();
      bool pos_not_found = (pos < 0) || (pos > (3));

      digitalWrite(LED_BUILTIN, HIGH);

      if (dataMsgBufferArray[0] == "/rpy")
      {
        if (pos_not_found)
          sendMsg = "0.00";
        else
          sendMsg = readRPY(pos);
        Serial.println(sendMsg);
      }

      if (dataMsgBufferArray[0] == "/quat")
      {
        if (pos_not_found)
          sendMsg = "0.00";
        else
          sendMsg = readQuat(pos);
        Serial.println(sendMsg);
      }

      else if (dataMsgBufferArray[0] == "/rpy-var")
      {
        if (dataMsgBufferArray[2] == ""){
          if (pos_not_found)
            sendMsg = "0.00";
          else
            sendMsg = readRPYVariance(pos);
        }
        else {
          if (pos_not_found)
            sendMsg = "0";
          else
            sendMsg = writeRPYVariance(pos, dataMsgBufferArray[2].toFloat());
        }
        Serial.println(sendMsg);
      }

      if (dataMsgBufferArray[0] == "/acc")
      {
        if (pos_not_found)
          sendMsg = "0.00";
        else
          sendMsg = readAcc(pos);
        Serial.println(sendMsg);
      }

      else if (dataMsgBufferArray[0] == "/acc-raw")
      {
        if (pos_not_found)
          sendMsg = "0.00";
        else
          sendMsg = readAccRaw(pos);
        Serial.println(sendMsg);
      }

      else if (dataMsgBufferArray[0] == "/acc-off")
      {
        if (dataMsgBufferArray[2] == ""){
          if (pos_not_found)
            sendMsg = "0.00";
          else
            sendMsg = readAccOffset(pos);
        }
        else {
          if (pos_not_found)
            sendMsg = "0";
          else
            sendMsg = writeAccOffset(pos, dataMsgBufferArray[2].toFloat());
        }
        Serial.println(sendMsg);
      }

      else if (dataMsgBufferArray[0] == "/acc-var")
      {
        if (dataMsgBufferArray[2] == ""){
          if (pos_not_found)
            sendMsg = "0.00";
          else
            sendMsg = readAccVariance(pos);
        }
        else {
          if (pos_not_found)
            sendMsg = "0";
          else
            sendMsg = writeAccVariance(pos, dataMsgBufferArray[2].toFloat());
        }
        Serial.println(sendMsg);
      }

      else if (dataMsgBufferArray[0] == "/gyro")
      {
        if (pos_not_found)
          sendMsg = "0.00";
        else
          sendMsg = readGyro(pos);
        Serial.println(sendMsg);
      }

      else if (dataMsgBufferArray[0] == "/gyro-raw")
      {
        if (pos_not_found)
          sendMsg = "0.00";
        else
          sendMsg = readGyroRaw(pos);
        Serial.println(sendMsg);
      }

      else if (dataMsgBufferArray[0] == "/gyro-off")
      {
        if (dataMsgBufferArray[2] == ""){
          if (pos_not_found)
            sendMsg = "0.00";
          else
            sendMsg = readGyroOffset(pos);
        }
        else {
          if (pos_not_found)
            sendMsg = "0";
          else
            sendMsg = writeGyroOffset(pos, dataMsgBufferArray[2].toFloat());
        }
        Serial.println(sendMsg);
      }

      else if (dataMsgBufferArray[0] == "/gyro-var")
      {
        if (dataMsgBufferArray[2] == ""){
          if (pos_not_found)
            sendMsg = "0.00";
          else
            sendMsg = readGyroVariance(pos);
        }
        else {
          if (pos_not_found)
            sendMsg = "0";
          else
            sendMsg = writeGyroVariance(pos, dataMsgBufferArray[2].toFloat());
        }
        Serial.println(sendMsg);
      }

      if (dataMsgBufferArray[0] == "/mag")
      {
        if (pos_not_found)
          sendMsg = "0.00";
        else
          sendMsg = readMag(pos);
        Serial.println(sendMsg);
      }

      else if (dataMsgBufferArray[0] == "/mag-raw")
      {
        if (pos_not_found)
          sendMsg = "0.00";
        else
          sendMsg = readMagRaw(pos);
        Serial.println(sendMsg);
      }

      else if (dataMsgBufferArray[0] == "/mag-bvect")
      {
        if (dataMsgBufferArray[2] == ""){
          if (pos_not_found)
            sendMsg = "0.00";
          else
            sendMsg = readMagHardOffset(pos);
        }
        else {
          if (pos_not_found)
            sendMsg = "0";
          else
            sendMsg = writeMagHardOffset(pos, dataMsgBufferArray[2].toFloat());
        }
        Serial.println(sendMsg);
      }

      else if (dataMsgBufferArray[0] == "/mag-amatR0")
      {
        if (dataMsgBufferArray[2] == ""){
          if (pos_not_found)
            sendMsg = "0.00";
          else
            sendMsg = readMagSoftOffset0(pos);
        }
        else {
          if (pos_not_found)
            sendMsg = "0";
          else
            sendMsg = writeMagSoftOffset0(pos, dataMsgBufferArray[2].toFloat());
        }
        Serial.println(sendMsg);
      }

      else if (dataMsgBufferArray[0] == "/mag-amatR1")
      {
        if (dataMsgBufferArray[2] == ""){
          if (pos_not_found)
            sendMsg = "0.00";
          else
            sendMsg = readMagSoftOffset1(pos);
        }
        else {
          if (pos_not_found)
            sendMsg = "0";
          else
            sendMsg = writeMagSoftOffset1(pos, dataMsgBufferArray[2].toFloat());
        }
        Serial.println(sendMsg);
      }

      else if (dataMsgBufferArray[0] == "/mag-amatR2")
      {
        if (dataMsgBufferArray[2] == ""){
          if (pos_not_found)
            sendMsg = "0.00";
          else
            sendMsg = readMagSoftOffset2(pos);
        }
        else {
          if (pos_not_found)
            sendMsg = "0";
          else
            sendMsg = writeMagSoftOffset2(pos, dataMsgBufferArray[2].toFloat());
        }
        Serial.println(sendMsg);
      }

      else if (dataMsgBufferArray[0] == "/i2c")
      {
        if (dataMsgBufferArray[2] == ""){
          sendMsg = getI2cAddress();
        }
        else {
          sendMsg = setI2cAddress(dataMsgBufferArray[2].toInt());
        }
        Serial.println(sendMsg);
      }

      else if (dataMsgBufferArray[0] == "/gain")
      {
        if (dataMsgBufferArray[2] == ""){
          sendMsg = getFilterGain();
        }
        else {
          sendMsg = setFilterGain(dataMsgBufferArray[2].toFloat());
        }
        Serial.println(sendMsg);
      }

      else if (dataMsgBufferArray[0] == "/frame-id")
      {
        if (dataMsgBufferArray[2] == ""){
          sendMsg = getWorldFrameId();
        }
        else {
          sendMsg = setWorldFrameId(dataMsgBufferArray[2].toInt());
        }
        Serial.println(sendMsg);
      }

      else if (dataMsgBufferArray[0] == "/reset")
      {
        sendMsg = triggerResetParams();
        Serial.println(sendMsg);
      }

      digitalWrite(LED_BUILTIN, LOW);
    }
    else
    {
      digitalWrite(LED_BUILTIN, HIGH);

      sendMsg = "0";
      Serial.println(sendMsg);

      digitalWrite(LED_BUILTIN, LOW);
    }

    sendMsg = "";
    dataMsg = "";
    dataMsgBuffer = "";
    dataMsgBufferArray[0] = "";
    dataMsgBufferArray[1] = "";
    dataMsgBufferArray[2] = "";
  } 
}

#endif