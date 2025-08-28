
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
        ax = eimuV2.readAcc(0);
        ay = eimuV2.readAcc(1);
        az = eimuV2.readAcc(2);

        gx = eimuV2.readGyro(0);
        gy = eimuV2.readGyro(1);
        gz = eimuV2.readGyro(2);
      }
      catch (...)
      {
      }

      std::cout << "ax: " << ax << std::fixed << std::setprecision(4);
      std::cout << "\tay: " << ax << std::fixed << std::setprecision(4);
      std::cout << "\taz: " << az << std::fixed << std::setprecision(4) << std::endl;
      std::cout << "gx: " << ax << std::fixed << std::setprecision(4);
      std::cout << "\tgy: " << ax << std::fixed << std::setprecision(4);
      std::cout << "\tgz: " << az << std::fixed << std::setprecision(4) << std::endl;
      std::cout << std::endl;
      
      prevTime = std::chrono::system_clock::now();
    }
  }
}