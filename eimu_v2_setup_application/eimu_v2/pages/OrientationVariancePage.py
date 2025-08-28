import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

import numpy as np
from termcolor import colored

from eimu_v2.globalParams import g


class OrientationVarianceFrame(tb.Frame):
  def __init__(self, parentFrame):
    super().__init__(master=parentFrame)

    # intialize parameter
    self.start_process = False
    self.loop_count = 0
    self.no_of_samples = 1000

    g.eimuV2.setWorldFrameId(1)

    self.r_arr = []
    self.p_arr = []
    self.y_arr = []

    self.label = tb.Label(self, text="COMPUTE ACC SENSOR VARIANCE", font=('Monospace',16, 'bold') ,bootstyle="dark")

    self.rValFrame = tb.Frame(self)
    self.pValFrame = tb.Frame(self)
    self.yValFrame = tb.Frame(self)

    r = g.eimuV2.readRPYVariance(0)
    p = g.eimuV2.readRPYVariance(1)
    y = g.eimuV2.readRPYVariance(2)

    self.rText = tb.Label(self.rValFrame, text="R-VARIANCE:", font=('Monospace',10, 'bold') ,bootstyle="danger")
    self.rVal = tb.Label(self.rValFrame, text=f'{r}', font=('Monospace',10), bootstyle="dark")

    self.pText = tb.Label(self.pValFrame, text="P-VARIANCE:", font=('Monospace',10, 'bold') ,bootstyle="success")
    self.pVal = tb.Label(self.pValFrame, text=f'{p}', font=('Monospace',10), bootstyle="dark")

    self.yText = tb.Label(self.yValFrame, text="Y-VARIANCE:", font=('Monospace',10, 'bold') ,bootstyle="primary")
    self.yVal = tb.Label(self.yValFrame, text=f'{y}', font=('Monospace',10), bootstyle="dark")
  
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
    self.rText.pack(side='left', fill='both')
    self.rVal.pack(side='left', expand=True, fill='both')

    self.pText.pack(side='left', fill='both')
    self.pVal.pack(side='left', expand=True, fill='both')

    self.yText.pack(side='left', fill='both')
    self.yVal.pack(side='left', expand=True, fill='both')
    
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

    self.rValFrame.pack(side='top', fill='x')
    self.pValFrame.pack(side='top', fill='x')
    self.yValFrame.pack(side='top', fill='x', pady=(0,20))

    # start process
    self.compute_variance()

  def reset_all_params(self):
    self.loop_count = 0
    self.no_of_samples = 1000

    self.r_arr = []
    self.p_arr = []
    self.y_arr = []

    percent = 0.0
    self.textVal.configure(text=f'{percent} %')
    self.progressBar['value'] = percent

  def read_cal_data(self):
    if self.start_process:
      self.no_of_samples = 1000

      self.rVal.configure(text="0.0")
      self.pVal.configure(text="0.0")
      self.yVal.configure(text="0.0")

      r = g.eimuV2.readRPY(0)
      p = g.eimuV2.readRPY(1)
      y = g.eimuV2.readRPY(2)

      self.r_arr.append(r)
      self.p_arr.append(p)
      self.y_arr.append(y)

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

    r_variance = np.var(self.r_arr)
    p_variance = np.var(self.p_arr)
    y_variance = np.var(self.y_arr)

    g.eimuV2.writeRPYVariance(0, r_variance)
    g.eimuV2.writeRPYVariance(1, p_variance)
    g.eimuV2.writeRPYVariance(2, y_variance)

    r_variance = g.eimuV2.readRPYVariance(0)
    p_variance = g.eimuV2.readRPYVariance(1)
    y_variance = g.eimuV2.readRPYVariance(2)

    self.rVal.configure(text=f'{r_variance}')
    self.pVal.configure(text=f'{p_variance}')
    self.yVal.configure(text=f'{y_variance}')

    rpy_covariance = [ r_variance, 0.0, 0.0, 0.0, p_variance, 0.0, 0.0, 0.0, y_variance]
    print(colored("\nOrientation Covariance:", 'green'))
    print(rpy_covariance)

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