
#include <sstream>
#include <iostream>
#include <unistd.h>

#include <chrono>

#include <iomanip>

#include "eimu_v2.hpp"

EIMU_V2 eimuV2;

void delay_ms(unsigned long milliseconds)
{
  usleep(milliseconds * 1000);
}

int main(int argc, char **argv)
{
  float ax, ay, az;
  float gx, gy, gz;

  auto prevTime = std::chrono::system_clock::now();
  std::chrono::duration<double> duration;
  float sampleTime = 0.01;

  std::string port = "/dev/ttyUSB0";
  eimuV2.connect(port);

  // wait for the eimuV2 to fully setup
  for (int i = 1; i <= 2; i += 1)
  {
    delay_ms(1000);
    std::cout << "configuring controller: " << i << " sec" << std::endl;
  }

  int worldFrameId = 1;
  eimuV2.setWorldFrameId(worldFrameId);
  worldFrameId = eimuV2.getWorldFrameId();
  if(worldFrameId == 1) std::cout << "ENU Frame" << std::endl;
  else if(worldFrameId == 0) std::cout << "NWU Frame" << std::endl;
  else if(worldFrameId == 2) std::cout << "NED Frame" << std::endl;

  prevTime = std::chrono::system_clock::now();

  while (true)
  {
    duration = (std::chrono::system_clock::now() - prevTime);
    if (duration.count() > sampleTime)
    {
      try
      {
        r = eimuV2.readRPY(0);
        p = eimuV2.readRPY(1);
        y = eimuV2.readRPY(2);

      }
      catch (...)
      {
      }

      std::cout << "roll: " << ax << std::fixed << std::setprecision(4);
      std::cout << "\tpitch: " << ax << std::fixed << std::setprecision(4);
      std::cout << "\tyaw: " << az << std::fixed << std::setprecision(4) << std::endl;
      
      prevTime = std::chrono::system_clock::now();
    }
  }
}