import time
from eimu_v2 import EIMU_V2

port = '/dev/ttyUSB0'
eimuV2 = EIMU_V2(port)

def main():
  for i in range(2):
    time.sleep(1.0)
    print(i+1, " sec")

  # change the reference frame to ENU frame (0 - NWU,  1 - ENU,  2 - NED)
  eimuV2.setWorldFrameId(1)

  # check the reference frame the eimuV2 is working in (0 - NWU,  1 - ENU,  2 - NED)
  ref_frame_id = eimuV2.getWorldFrameId()

  if ref_frame_id == 0:
    print("Reference Frame is North-West-Up (NWU)")
  elif ref_frame_id == 1:
    print("Reference Frame is East-North-Up (ENU)")
  elif ref_frame_id == 2:
    print("Reference Frame is North-East-Down (NED)")

  prevTime = time.time()
  sampleTime = 0.01

  while True:
    if time.time() - prevTime > sampleTime:
      try:
        r = eimuV2.readRPY(0)
        p = eimuV2.readRPY(1)
        y = eimuV2.readRPY(2)

        print(f"r: {r}\tp: {p}\ty: {y}")
      except:
        pass
      
      prevTime = time.time()

if __name__ == "__main__":
  main()