import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

import numpy as np
from termcolor import colored

from eimu_v2.globalParams import g


class GyroVarianceFrame(tb.Frame):
  def __init__(self, parentFrame):
    super().__init__(master=parentFrame)

    # intialize parameter
    self.start_process = False
    self.loop_count = 0
    self.no_of_samples = 1000

    g.eimuV2.setWorldFrameId(1)

    self.gyrox_arr = []
    self.gyroy_arr = []
    self.gyroz_arr = []

    self.label = tb.Label(self, text="COMPUTE GYRO SENSOR VARIANCE", font=('Monospace',16, 'bold') ,bootstyle="dark")

    self.gxValFrame = tb.Frame(self)
    self.gyValFrame = tb.Frame(self)
    self.gzValFrame = tb.Frame(self)

    gx = g.eimuV2.readGyroVariance(0)
    gy = g.eimuV2.readGyroVariance(1)
    gz = g.eimuV2.readGyroVariance(2)

    self.gxText = tb.Label(self.gxValFrame, text="GX-VARIANCE:", font=('Monospace',10, 'bold') ,bootstyle="danger")
    self.gxVal = tb.Label(self.gxValFrame, text=f'{gx}', font=('Monospace',10), bootstyle="dark")

    self.gyText = tb.Label(self.gyValFrame, text="GY-VARIANCE:", font=('Monospace',10, 'bold') ,bootstyle="success")
    self.gyVal = tb.Label(self.gyValFrame, text=f'{gy}', font=('Monospace',10), bootstyle="dark")

    self.gzText = tb.Label(self.gzValFrame, text="GZ-VARIANCE:", font=('Monospace',10, 'bold') ,bootstyle="primary")
    self.gzVal = tb.Label(self.gzValFrame, text=f'{gz}', font=('Monospace',10), bootstyle="dark")
  
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
    self.gxText.pack(side='left', fill='both')
    self.gxVal.pack(side='left', expand=True, fill='both')

    self.gyText.pack(side='left', fill='both')
    self.gyVal.pack(side='left', expand=True, fill='both')

    self.gzText.pack(side='left', fill='both')
    self.gzVal.pack(side='left', expand=True, fill='both')
    
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

    self.gxValFrame.pack(side='top', fill='x')
    self.gyValFrame.pack(side='top', fill='x')
    self.gzValFrame.pack(side='top', fill='x', pady=(0,20))

    # start process
    self.compute_variance()

  def reset_all_params(self):
    self.loop_count = 0
    self.no_of_samples = 1000

    self.gyrox_arr = []
    self.gyroy_arr = []
    self.gyroz_arr = []

    percent = 0.0
    self.textVal.configure(text=f'{percent} %')
    self.progressBar['value'] = percent

  def read_cal_data(self):
    if self.start_process:
      self.no_of_samples = 1000

      self.gxVal.configure(text="0.0")
      self.gyVal.configure(text="0.0")
      self.gzVal.configure(text="0.0")

      gyrox_cal = g.eimuV2.readGyro(0)
      gyroy_cal = g.eimuV2.readGyro(1)
      gyroz_cal = g.eimuV2.readGyro(2)

      self.gyrox_arr.append(gyrox_cal)
      self.gyroy_arr.append(gyroy_cal)
      self.gyroz_arr.append(gyroz_cal)

      self.loop_count += 1
      percent = (self.loop_count*100)/self.no_of_samples
      self.textVal.configure(text=f'{percent} %')
      self.progressBar['value'] = percent

      if percent >= 100.0:
        percent = 100.0
        self.textVal.configure(text=f'{percent} %')
        self.progressBar['value'] = percent
        self.print_computed_variance()
      else:
        self.canvas.after(1, self.read_cal_data)

    else:
      self.reset_all_params()
      self.canvas.after(10, self.compute_variance)

  def print_computed_variance(self):

    gyrox_variance = np.var(self.gyrox_arr)
    gyroy_variance = np.var(self.gyroy_arr)
    gyroz_variance = np.var(self.gyroz_arr)

    g.eimuV2.writeGyroVariance(0, gyrox_variance)
    g.eimuV2.writeGyroVariance(1, gyroy_variance)
    g.eimuV2.writeGyroVariance(2, gyroz_variance)

    gyrox_variance = g.eimuV2.readGyroVariance(0)
    gyroy_variance = g.eimuV2.readGyroVariance(1)
    gyroz_variance = g.eimuV2.readGyroVariance(2)

    self.gxVal.configure(text=f'{gyrox_variance}')
    self.gyVal.configure(text=f'{gyroy_variance}')
    self.gzVal.configure(text=f'{gyroz_variance}')

    gyro_covariance = [ gyrox_variance, 0.0, 0.0, 0.0, gyroy_variance, 0.0, 0.0, 0.0, gyroz_variance]
    print(colored("\nAngular Velocity Covariance:", 'green'))
    print(gyro_covariance)

  def compute_variance(self):
    if self.start_process:
      self.reset_all_params()
      self.read_cal_data()
    else:
      self.reset_all_params()
      self.canvas.after(10, self.compute_variance)

  def change_btn_state(self):
    if self.start_process:
      self.start_process = False
      self.pressButton.configure(text='START')

    else:
      self.start_process = True
      self.pressButton.configure(text='STOP')