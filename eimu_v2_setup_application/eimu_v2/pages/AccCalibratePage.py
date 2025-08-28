# REFERENCE: https://learn.adafruit.com/adafruit-sensorlab-gyroscope-calibration/gyro-calibration-with-jupyter
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

import matplotlib.pyplot as plt
from collections import deque
import numpy as np
from termcolor import colored

from eimu_v2.globalParams import g


class AccCalibrateFrame(tb.Frame):
  def __init__(self, parentFrame):
    super().__init__(master=parentFrame)

    # intialize parameter
    self.start_process = False
    self.loop_count = 0
    self.no_of_samples = 1000

    g.eimuV2.setWorldFrameId(1)

    self.acc_x = deque(maxlen=self.no_of_samples)
    self.acc_y = deque(maxlen=self.no_of_samples)
    self.acc_z = deque(maxlen=self.no_of_samples)

    self.label = tb.Label(self, text="CALIBRATE ACCELEROMETER SENSOR", font=('Monospace',16, 'bold') ,bootstyle="dark")
    
    self.axValFrame = tb.Frame(self)
    self.ayValFrame = tb.Frame(self)
    self.azValFrame = tb.Frame(self)

    ax = g.eimuV2.readAccOffset(0)
    ay = g.eimuV2.readAccOffset(1)
    az = g.eimuV2.readAccOffset(2)

    self.axText = tb.Label(self.axValFrame, text="AX-OFFSET:", font=('Monospace',10, 'bold') ,bootstyle="danger")
    self.axVal = tb.Label(self.axValFrame, text=f'{ax}', font=('Monospace',10), bootstyle="dark")

    self.ayText = tb.Label(self.ayValFrame, text="AY-OFFSET:", font=('Monospace',10, 'bold') ,bootstyle="success")
    self.ayVal = tb.Label(self.ayValFrame, text=f'{ay}', font=('Monospace',10), bootstyle="dark")

    self.azText = tb.Label(self.azValFrame, text="AZ-OFFSET:", font=('Monospace',10, 'bold') ,bootstyle="primary")
    self.azVal = tb.Label(self.azValFrame, text=f'{az}', font=('Monospace',10), bootstyle="dark")
  
    #create widgets to be added to the Fame
    percent = 0.0
    self.textVal = tb.Label(self, text=f'{percent} %', font=('Monospace',20, 'bold'), bootstyle="primary")
    self.progressBar = tb.Progressbar(self, bootstyle="danger striped", mode='determinate',
                                      maximum=100, length=200, value=0.0)

    buttonStyle = tb.Style()
    buttonStyleName = 'primary.TButton'
    buttonStyle.configure(buttonStyleName, font=('Monospace',15,'bold'))
    self.pressButton = tb.Button(self, text="START", style=buttonStyleName,
                                 command=self.change_btn_state)
    
    self.canvasFrame = tb.Frame(self)
    

    #add created widgets to displayFrame
    self.axText.pack(side='left', fill='both')
    self.axVal.pack(side='left', expand=True, fill='both')

    self.ayText.pack(side='left', fill='both')
    self.ayVal.pack(side='left', expand=True, fill='both')

    self.azText.pack(side='left', fill='both')
    self.azVal.pack(side='left', expand=True, fill='both')
    
    #add created widgets to Frame
    self.label.pack(side='top', pady=(20,50))
    self.textVal.pack(side='top', expand=True, fill='y')
    self.progressBar.pack(side='top', expand=True, fill='x', padx=50)
    self.pressButton.pack(side='top', fill='y')
    self.canvasFrame.pack(side='top', expand=True, fill='both', pady=(10,0))

    #create widgets to be added to the canvasFame
    self.canvas = tb.Canvas(self.canvasFrame, width=300, height=2, autostyle=False ,bg="#FFFFFF", relief='solid')

    #add created widgets to canvasFame
    self.canvas.pack(side='left', expand=True, fill='both', pady=(0,20))

    self.axValFrame.pack(side='top', fill='x')
    self.ayValFrame.pack(side='top', fill='x')
    self.azValFrame.pack(side='top', fill='x')

    # start process
    self.calibrate_imu()

  def reset_all_params(self):
    self.loop_count = 0
    self.no_of_samples = 1000

    self.acc_x = deque(maxlen=self.no_of_samples)
    self.acc_y = deque(maxlen=self.no_of_samples)
    self.acc_z = deque(maxlen=self.no_of_samples)

    percent = 0.0
    self.textVal.configure(text=f'{percent} %')
    self.progressBar['value'] = percent

  def read_data(self):
    if self.start_process:

      self.axVal.configure(text="0.0")
      self.ayVal.configure(text="0.0")
      self.azVal.configure(text="0.0")

      ax = g.eimuV2.readAccRaw(0)
      ay = g.eimuV2.readAccRaw(1)
      az = g.eimuV2.readAccRaw(2)

      self.acc_x.append(ax)
      self.acc_y.append(ay)
      self.acc_z.append(az)

      self.loop_count += 1
      percent = (self.loop_count*100)/self.no_of_samples
      self.textVal.configure(text=f'{percent} %')
      self.progressBar['value'] = percent

      if percent >= 100.0:
        percent = 100.0
        self.textVal.configure(text=f'{percent} %')
        self.progressBar['value'] = percent
        self.plot_calibrated_data()
      else:
        self.canvas.after(1, self.read_data)

    else:
      self.reset_all_params()
      self.canvas.after(10, self.calibrate_imu)

  def plot_calibrated_data(self):
    ax_offset = self.average(self.acc_x)
    ay_offset = self.average(self.acc_y)
    az_offset = (self.average(self.acc_z) - 9.8)

    g.eimuV2.writeAccOffset(0, ax_offset)
    g.eimuV2.writeAccOffset(1, ay_offset)
    g.eimuV2.writeAccOffset(2, az_offset)

    ax_offset = g.eimuV2.readAccOffset(0)
    ay_offset = g.eimuV2.readAccOffset(1)
    az_offset = g.eimuV2.readAccOffset(2)

    self.axVal.configure(text=f'{ax_offset}')
    self.ayVal.configure(text=f'{ay_offset}')
    self.azVal.configure(text=f'{az_offset}')
    
    acc_calibration = [ ax_offset, ay_offset, az_offset ]

    print(colored("\nacc offsets in m/s^2:", 'green'))
    print(acc_calibration)

    fig, (accUncal, accCal) = plt.subplots(nrows=2)

    # Clear all axis
    accUncal.cla()
    accCal.cla()
    t = np.linspace(0, len(self.acc_x), len(self.acc_x))


    # plot uncalibrated data
    accUncal.plot(t, self.acc_x, color='r')
    accUncal.plot(t, self.acc_y, color='g')
    accUncal.plot(t, self.acc_z, color='b')
    accUncal.title.set_text("Uncalibrated Acc")
    accUncal.set(ylabel='g')

    accUncal.grid(which = "major", linewidth = 0.5)
    accUncal.grid(which = "minor", linewidth = 0.2)
    accUncal.minorticks_on()

    # plot calibrated data
    accCal.plot(t, [x - acc_calibration[0] for x in self.acc_x], color='r')
    accCal.plot(t, [y - acc_calibration[1] for y in self.acc_y], color='g')
    accCal.plot(t, [z - acc_calibration[2] for z in self.acc_z], color='b')
    accCal.title.set_text("Calibrated Acc")
    accCal.set(ylabel='m/s/s')

    accCal.grid(which = "major", linewidth = 0.5)
    accCal.grid(which = "minor", linewidth = 0.2)
    accCal.minorticks_on()

    fig.tight_layout()
    plt.show()

  def calibrate_imu(self):
    if self.start_process:
      self.reset_all_params()
      self.read_data()
    else:
      self.reset_all_params()
      self.canvas.after(10, self.calibrate_imu)

  def change_btn_state(self):
    if self.start_process:
      self.start_process = False
      self.pressButton.configure(text='START')

    else:
      self.start_process = True
      self.pressButton.configure(text='STOP')

  def average(self, val):
      ans = 0
      for i in val:
        ans= ans + i
      
      ans = ans/len(val)
      
      return ans