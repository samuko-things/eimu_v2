import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from eimu_v2.globalParams import g
from eimu_v2.components.SetValueFrame import SetValueFrame
from eimu_v2.components.SelectValueFrame import SelectValueFrame



class ImuVisualizeFrame(tb.Frame):
  def __init__(self, parentFrame):
    super().__init__(master=parentFrame)

    self.fig, self.ax = None, None

    self.world_axis_x_color = '#a00000'
    self.world_axis_y_color = 'green'
    self.world_axis_z_color = '#0000a0'

    self.world_axis_line_width = str(4.0)

    self.sensor_axis_x_color = 'red'
    self.sensor_axis_y_color = '#00a000'
    self.sensor_axis_z_color = 'blue'

    self.sensor_axis_line_width = str(4.0)

    # self.plot_elevation_angle = 60 
    # self.plot_horizontal_angle = 60
    
    g.eimuV2.setWorldFrameId(1)

    self.label = tb.Label(self, text="VIZUALIZE IMU DATA", font=('Monospace',16, 'bold') ,bootstyle="dark")
  
    #create widgets to be added to the Fame
    g.frameId = int(g.eimuV2.getWorldFrameId())
    self.selectFrameId = SelectValueFrame(self, keyTextInit=f"REFERENCE_FRAME: ", valTextInit=g.frameList[g.frameId],
                                          initialComboValues=g.frameList, middileware_func=self.selectFrameIdFunc)
    
    g.filterGain = g.eimuV2.getFilterGain()
    self.setFilterGain = SetValueFrame(self, keyTextInit="FILTER_GAIN: ", valTextInit=g.filterGain,
                                middleware_func=self.setFilterGainFunc)
    
    buttonStyle = tb.Style()
    buttonStyleName = 'primary.TButton'
    buttonStyle.configure(buttonStyleName, font=('Monospace',12,'bold'))

    self.button = tb.Button(self, text="READ IMU DATA", style=buttonStyleName,
                             padding=20, command=self.runVisualization)
    

    self.imuDisplayFrame = tb.Frame(self)

    self.orientationValFrame = tb.Frame(self.imuDisplayFrame)
    self.rValFrame = tb.Frame(self.orientationValFrame)
    self.pValFrame = tb.Frame(self.orientationValFrame)
    self.yValFrame = tb.Frame(self.orientationValFrame)

    self.accelerationValFrame = tb.Frame(self.imuDisplayFrame)
    self.axValFrame = tb.Frame(self.accelerationValFrame)
    self.ayValFrame = tb.Frame(self.accelerationValFrame)
    self.azValFrame = tb.Frame(self.accelerationValFrame)

    self.angularVelValFrame = tb.Frame(self.imuDisplayFrame)
    self.gxValFrame = tb.Frame(self.angularVelValFrame)
    self.gyValFrame = tb.Frame(self.angularVelValFrame)
    self.gzValFrame = tb.Frame(self.angularVelValFrame)

    r = g.eimuV2.readRPY(0)
    p = g.eimuV2.readRPY(1)
    y = g.eimuV2.readRPY(2)

    self.rText = tb.Label(self.rValFrame, text="R:", font=('Monospace',10, 'bold') ,bootstyle="danger")
    self.rVal = tb.Label(self.rValFrame, text=f'{r}', font=('Monospace',10), bootstyle="dark")

    self.pText = tb.Label(self.pValFrame, text="P:", font=('Monospace',10, 'bold') ,bootstyle="success")
    self.pVal = tb.Label(self.pValFrame, text=f'{p}', font=('Monospace',10), bootstyle="dark")

    self.yText = tb.Label(self.yValFrame, text="Y:", font=('Monospace',10, 'bold') ,bootstyle="primary")
    self.yVal = tb.Label(self.yValFrame, text=f'{y}', font=('Monospace',10), bootstyle="dark")

    ax = g.eimuV2.readAcc(0)
    ay = g.eimuV2.readAcc(1)
    az = g.eimuV2.readAcc(2)

    self.axText = tb.Label(self.axValFrame, text="AX:", font=('Monospace',10, 'bold') ,bootstyle="danger")
    self.axVal = tb.Label(self.axValFrame, text=f'{ax}', font=('Monospace',10), bootstyle="dark")

    self.ayText = tb.Label(self.ayValFrame, text="AY:", font=('Monospace',10, 'bold') ,bootstyle="success")
    self.ayVal = tb.Label(self.ayValFrame, text=f'{ay}', font=('Monospace',10), bootstyle="dark")

    self.azText = tb.Label(self.azValFrame, text="AZ:", font=('Monospace',10, 'bold') ,bootstyle="primary")
    self.azVal = tb.Label(self.azValFrame, text=f'{az}', font=('Monospace',10), bootstyle="dark")

    gx = g.eimuV2.readGyro(0)
    gy = g.eimuV2.readGyro(1)
    gz = g.eimuV2.readGyro(2)

    self.gxText = tb.Label(self.axValFrame, text="GX:", font=('Monospace',10, 'bold') ,bootstyle="danger")
    self.gxVal = tb.Label(self.axValFrame, text=f'{gx}', font=('Monospace',10), bootstyle="dark")

    self.gyText = tb.Label(self.ayValFrame, text="GY:", font=('Monospace',10, 'bold') ,bootstyle="success")
    self.gyVal = tb.Label(self.ayValFrame, text=f'{gy}', font=('Monospace',10), bootstyle="dark")

    self.gzText = tb.Label(self.azValFrame, text="GZ:", font=('Monospace',10, 'bold') ,bootstyle="primary")
    self.gzVal = tb.Label(self.azValFrame, text=f'{gz}', font=('Monospace',10), bootstyle="dark")
    

    #add created widgets to displayFrame
    self.rText.pack(side='left', fill='both')
    self.rVal.pack(side='left', expand=True, fill='both')

    self.pText.pack(side='left', fill='both')
    self.pVal.pack(side='left', expand=True, fill='both')

    self.yText.pack(side='left', fill='both')
    self.yVal.pack(side='left', expand=True, fill='both')

    self.axText.pack(side='left', fill='both')
    self.axVal.pack(side='left', expand=True, fill='both')

    self.ayText.pack(side='left', fill='both')
    self.ayVal.pack(side='left', expand=True, fill='both')

    self.azText.pack(side='left', fill='both')
    self.azVal.pack(side='left', expand=True, fill='both')

    self.gxText.pack(side='left', fill='both')
    self.gxVal.pack(side='left', expand=True, fill='both')

    self.gyText.pack(side='left', fill='both')
    self.gyVal.pack(side='left', expand=True, fill='both')

    self.gzText.pack(side='left', fill='both')
    self.gzVal.pack(side='left', expand=True, fill='both')

    #add created widgets to Frame
    self.label.pack(side='top', pady=(20,20))
    self.selectFrameId.pack(side='top', fill='y', pady=(30,0))
    self.setFilterGain.pack(side='top', fill='y', pady=(30,0))
    self.button.pack(side='top', fill='y', pady=(50,0))
    self.imuDisplayFrame.pack(side='top', fill='x', pady=(50,0))

    self.orientationValFrame.pack(side='left', expand=True, fill='both')
    self.accelerationValFrame.pack(side='left', expand=True, fill='both')
    self.angularVelValFrame.pack(side='left', expand=True, fill='both')

    self.rValFrame.pack(side='top', fill='x')
    self.pValFrame.pack(side='top', fill='x')
    self.yValFrame.pack(side='top', fill='x')

    self.axValFrame.pack(side='top', fill='x')
    self.ayValFrame.pack(side='top', fill='x')
    self.azValFrame.pack(side='top', fill='x')

    self.gxValFrame.pack(side='top', fill='x')
    self.gyValFrame.pack(side='top', fill='x')
    self.gzValFrame.pack(side='top', fill='x')    
  
    ############################################


  def setFilterGainFunc(self, text):
    try:
      if text:
        isSuccessful = g.eimuV2.setFilterGain(float(text))
        val = g.eimuV2.getFilterGain()
        g.filterGain = val
    except:
      pass
  
    return g.filterGain
  

  def selectFrameIdFunc(self, frame_val_str):
    try:
      if frame_val_str:
        
        if frame_val_str == g.frameList[0]:
          isSuccessful = g.eimuV2.setWorldFrameId(0)
          
        elif frame_val_str == g.frameList[1]:
          isSuccessful = g.eimuV2.setWorldFrameId(1)
        
        elif frame_val_str == g.frameList[2]:
          isSuccessful = g.eimuV2.setWorldFrameId(2)

    except:
      pass

    g.frameId = int(g.eimuV2.getWorldFrameId())
    return g.frameList[g.frameId]


  def onClose(self,event): 
    plt.close()
    self.fig, self.ax = None, None 


  def animate(self,i):
    try:
      r = g.eimuV2.readRPY(0)
      p = g.eimuV2.readRPY(1)
      y = g.eimuV2.readRPY(2)
      
      self.rVal.configure(text=f"{r}")
      self.pVal.configure(text=f"{p}")
      self.yVal.configure(text=f"{y}")

      ax = g.eimuV2.readAcc(0)
      ay = g.eimuV2.readAcc(1)
      az = g.eimuV2.readAcc(2)
      
      self.axVal.configure(text=f"{ax}")
      self.ayVal.configure(text=f"{ay}")
      self.azVal.configure(text=f"{az}")

      gx = g.eimuV2.readGyro(0)
      gy = g.eimuV2.readGyro(1)
      gz = g.eimuV2.readGyro(2)
      
      self.gxVal.configure(text=f"{gx}")
      self.gyVal.configure(text=f"{gy}")
      self.gzVal.configure(text=f"{gz}")

      #-----------------------------------------------------------------------
      ##### convert rpy to DCM #####################
      DCM = [[np.cos(p)*np.cos(y), np.cos(p)*np.sin(y), -1.0*np.sin(p)], # cθcψ, cθsψ, −sθ
             [(np.sin(r)*np.sin(p)*np.cos(y)) - (np.cos(r)*np.sin(y)), (np.sin(r)*np.sin(p)*np.sin(y)) + (np.cos(r)*np.cos(y)), np.sin(r)*np.cos(p)], # sϕsθcψ - cϕsψ, sϕsθsψ + cϕcψ, sϕcθ
             [(np.cos(r)*np.sin(p)*np.cos(y)) + (np.sin(r)*np.sin(y)), (np.cos(r)*np.sin(p)*np.sin(y)) - (np.sin(r)*np.cos(y)), np.cos(r)*np.cos(p)]] # cϕsθcψ + sϕsψ, cϕsθsψ - sϕcψ, cϕcθ
      
      ##### get the IMU sensor coordinate vector from the DCM #####################
      x_vect = DCM[0]
      y_vect = DCM[1]
      z_vect = DCM[2]
      #----------------------------------------------------------------------



      # Clear all axis
      self.ax.cla()
      
      self.ax.set_xlim(-1.0, 1.0)
      self.ax.set_ylim(-1.0, 1.0)
      self.ax.set_zlim(-1.0, 1.0)
      self.ax.grid(False)
      # self.ax.view_init(self.plot_elevation_angle, self.plot_horizontal_angle)
      
      # defining world axes
      x0 = [0, 1]
      x1 = [0, 0]
      x2 = [0, 0]  
      self.ax.plot(x0, x1, x2, c=self.world_axis_x_color, lw=self.world_axis_line_width)

      y0 = [0, 0]
      y1 = [0, 1]
      y2 = [0, 0]  
      self.ax.plot(y0, y1, y2, c=self.world_axis_y_color, lw=self.world_axis_line_width)

      z0 = [0, 0]
      z1 = [0, 0]
      z2 = [0, 1]  
      self.ax.plot(z0, z1, z2, c=self.world_axis_z_color, lw=self.world_axis_line_width)


      # defining sensor axes
      x0 = [0, x_vect[0]]
      x1 = [0, x_vect[1]]
      x2 = [0, x_vect[2]]  
      self.ax.plot(x0, x1, x2, c=self.sensor_axis_x_color, lw=self.sensor_axis_line_width)

      y0 = [0, y_vect[0]]
      y1 = [0, y_vect[1]]
      y2 = [0, y_vect[2]]  
      self.ax.plot(y0, y1, y2, c=self.sensor_axis_y_color, lw=self.sensor_axis_line_width)

      z0 = [0, z_vect[0]]
      z1 = [0, z_vect[1]]
      z2 = [0, z_vect[2]]  
      self.ax.plot(z0, z1, z2, c=self.sensor_axis_z_color, lw=self.sensor_axis_line_width)
        
        
    ##    # Pause the plot for INTERVAL seconds 
    ##    plt.pause(INTERVAL)
    except:
      pass


  def runVisualization(self):
    self.fig = plt.figure()
    self.ax = self.fig.add_subplot(111, projection='3d')

    self.ax.set_xlim(-1.0, 1.0)
    self.ax.set_ylim(-1.0, 1.0)
    self.ax.set_zlim(-1.0, 1.0)
    self.ax.grid(False)
    # self.ax.view_init(self.plot_elevation_angle, self.plot_horizontal_angle)
    
    # defining axes
    x0 = [0, 1]
    x1 = [0, 0]
    x2 = [0, 0]  
    self.ax.plot(x0, x1, x2, c=self.world_axis_x_color, lw=self.world_axis_line_width)

    y0 = [0, 0]
    y1 = [0, 1]
    y2 = [0, 0]  
    self.ax.plot(y0, y1, y2, c=self.world_axis_y_color, lw=self.world_axis_line_width)

    z0 = [0, 0]
    z1 = [0, 0]
    z2 = [0, 1]  
    self.ax.plot(z0, z1, z2, c=self.world_axis_z_color, lw=self.world_axis_line_width)

    self.fig.canvas.mpl_connect('close_event', self.onClose)
    self.anim = FuncAnimation(self.fig, self.animate, frames = np.arange(0, 1000000, 1), interval=50)
    plt.show()