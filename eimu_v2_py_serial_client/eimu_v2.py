import serial
import time

class EIMU_V2:
    def __init__(self, port, baud=115200, timeOut=0.1):
        self.ser = serial.Serial(port, baud, timeout=timeOut)
    
    def send_and_receive(self, msg_cmd):
        data = ""
        prev_time = time.time()
        while data=="":
            try:
                self.ser.write(msg_cmd.encode())   # send a single or multiple byte    
                data = self.ser.readline().decode().strip()
                if time.time()-prev_time > 2.0:
                    raise Exception("[Timeout] No response from ESP32")
            except:
                print("[Timeout] No response from ESP32")
        return data
    
    def send(self, cmd_route, motor_no, val):
        cmd_str = cmd_route+","+str(motor_no)+","+str(val)
        data = self.send_and_receive(cmd_str)
        if data == "1":
            return True
        else:
            return False
  
    def get(self, cmd_route, motor_no):
        cmd_str = cmd_route+","+str(motor_no)
        data = self.send_and_receive(cmd_str).split(',')
        if len(data)==1:
            return float(data[0])
        elif len(data)==2:
            return float(data[0]), float(data[1])
        
    def setWorldFrameId(self, id):
        res = self.send("/frame-id", -1, id)
        return res
    
    def getWorldFrameId(self):
        id = self.get("/frame-id", -1)
        return id
    
    def getFilterGain(self):
        gain = self.get("/gain", -1)
        return gain
    
    def readQuat(self, pos_no):
        val = self.get("/quat", pos_no)
        return val
    
    def readRPY(self, pos_no):
        val = self.get("/rpy", pos_no)
        return val
    
    def readRPYVariance(self, pos_no):
        val = self.get("/rpy-var", pos_no)
        return val
    
    def readAcc(self, pos_no):
        val = self.get("/acc", pos_no)
        return val
    
    def readAccVariance(self, pos_no):
        val = self.get("/acc-var", pos_no)
        return val
    
    def readGyro(self, pos_no):
        val = self.get("/gyro", pos_no)
        return val
    
    def readGyroVariance(self, pos_no):
        val = self.get("/gyro-var", pos_no)
        return val
    
    def readMag(self, pos_no):
        val = self.get("/mag", pos_no)
        return val