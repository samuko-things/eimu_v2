import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from eimu_v2.pages.MagCalibratePage import MagCalibrateFrame
from eimu_v2.pages.GyroCalibratePage import GyroCalibrateFrame
from eimu_v2.pages.AccCalibratePage import AccCalibrateFrame
from eimu_v2.pages.ImuVisualizePage import ImuVisualizeFrame
# from eimu_v2.pages.ComputeAngleVariancePage import ComputeAngleVarFrame
from eimu_v2.pages.GyroVariancePage import GyroVarianceFrame 
from eimu_v2.pages.AccVariancePage import AccVarianceFrame 
from eimu_v2.pages.I2CSetupPage import I2CSetupFrame
from eimu_v2.pages.ResetSetupPage import ResetSetupFrame


class MainAppFrame(tb.Frame):
  def __init__(self, parentFrame):
    super().__init__(master=parentFrame)


    # SIDEBAR NAVIGATION FRAME
    self.sideNavFrame = tb.LabelFrame(self, borderwidth=10)

    # MIAN CONTENT FRAME
    self.mainContentFrame = tb.Frame(self)


    #create widgets to be added to the sideNavFrame
    self.label = tb.Label(self.sideNavFrame, text="MENU", font=('Monospace',20, 'bold') ,bootstyle="secondary")

    buttonStyle = tb.Style()
    buttonStyleName = 'primary.Link.TButton'
    buttonStyle.configure(buttonStyleName, font=('Monospace',12, 'bold'))

    
    self.button1 = tb.Button(self.sideNavFrame, text="MAG CALIBRATION", style=buttonStyleName,
                             command= lambda: self.displayPage(self.button1, self.displayMagCalibratePage))
    
    self.button2 = tb.Button(self.sideNavFrame, text="GYRO CALIBRATION", style=buttonStyleName,
                             command= lambda: self.displayPage(self.button2, self.displayGyroCalibratePage))
    
    self.button3 = tb.Button(self.sideNavFrame, text="ACC CALIBRATION", style=buttonStyleName,
                             command= lambda: self.displayPage(self.button3, self.displayAccCalibratePage))
    
    self.button4 = tb.Button(self.sideNavFrame, text="VIZUALIZE IMU DATA", style=buttonStyleName,
                             command= lambda: self.displayPage(self.button4, self.displayImuVisualizePage))
    
    # self.button5 = tb.Button(self.sideNavFrame, text="RPY VARIANCE", style=buttonStyleName,
    #                          command= lambda: self.displayPage(self.button5, self.displayComputeAngleVariancePage))
    
    self.button6 = tb.Button(self.sideNavFrame, text="GYRO VARIANCE", style=buttonStyleName,
                             command= lambda: self.displayPage(self.button6, self.displayGyroVariancePage))
    
    self.button7 = tb.Button(self.sideNavFrame, text="ACC VARIANCE", style=buttonStyleName,
                             command= lambda: self.displayPage(self.button7, self.displayAccVariancePage))
    
    self.button8 = tb.Button(self.sideNavFrame, text="I2C SETUP", style=buttonStyleName,
                             command= lambda: self.displayPage(self.button8, self.displayI2CSetupPage))
    
    self.button9 = tb.Button(self.sideNavFrame, text="RESET PARAMS", style=buttonStyleName,
                             command= lambda: self.displayPage(self.button9, self.displayResetPage))
    
    
    
    
    
    
    # add widget to sideNavFrame
    self.label.pack(side="top", fill="x", padx=(40,0), pady=(0,40))
    self.button1.pack(side="top", fill="x", padx=5, pady=(0,5))
    self.button2.pack(side="top", fill="x", padx=5, pady=(0,5))
    self.button3.pack(side="top", fill="x", padx=5, pady=(0,40))
    self.button4.pack(side="top", fill="x", padx=5, pady=(0,40))
    # self.button5.pack(side="top", fill="x", padx=5, pady=(0,5))
    self.button6.pack(side="top", fill="x", padx=5, pady=(0,5))
    self.button7.pack(side="top", fill="x", padx=5, pady=(0,40))
    self.button8.pack(side="top", fill="x", padx=5, pady=(0,5))
    self.button9.pack(side="top", fill="x", padx=5, pady=(0,5))

    
    ############Initialize the mainContentFrame ################
    self.displayPage(self.button9, self.displayResetPage)
    ############################################################


    #add framed widgets to MainAppFrame
    self.sideNavFrame.pack(side="left", fill="y", padx=10)
    self.mainContentFrame.pack(side="left", expand=True, fill="both", padx=5)


  
  def enable_all_nav_buttons(self):
    self.button1.configure(state="normal")
    self.button2.configure(state="normal")
    self.button3.configure(state="normal")
    self.button4.configure(state="normal")
    # self.button5.configure(state="normal")
    self.button6.configure(state="normal")
    self.button7.configure(state="normal")
    self.button8.configure(state="normal")
    self.button9.configure(state="normal")
  
  def displayPage(self, button, page):
    self.enable_all_nav_buttons()
    button.configure(state='disabled') # disable the clicked nav button
    self.delete_pages()
    page()

  def delete_pages(self):
    for frame in self.mainContentFrame.winfo_children():
      frame.destroy()

  def displayMagCalibratePage(self):
    self.magCalibrateFrame = MagCalibrateFrame(self.mainContentFrame)
    self.magCalibrateFrame.pack(side="left", expand=True, fill="both")

  def displayGyroCalibratePage(self):
    self.gyroCalibrateFrame = GyroCalibrateFrame(self.mainContentFrame)
    self.gyroCalibrateFrame.pack(side="left", expand=True, fill="both")

  def displayAccCalibratePage(self):
    self.accCalibrateFrame = AccCalibrateFrame(self.mainContentFrame)
    self.accCalibrateFrame.pack(side="left", expand=True, fill="both")
  
  def displayImuVisualizePage(self):
    self.imuVisualizeFrame = ImuVisualizeFrame(self.mainContentFrame)
    self.imuVisualizeFrame.pack(side="left", expand=True, fill="both")

  # def displayComputeAngleVariancePage(self):
  #   self.computeAngleVarianceFrame = ComputeAngleVarFrame(self.mainContentFrame)
  #   self.computeAngleVarianceFrame.pack(side="left", expand=True, fill="both")

  def displayGyroVariancePage(self):
    self.gyroVarianceFrame = GyroVarianceFrame(self.mainContentFrame)
    self.gyroVarianceFrame.pack(side="left", expand=True, fill="both")

  def displayAccVariancePage(self):
    self.accVarianceFrame = AccVarianceFrame(self.mainContentFrame)
    self.accVarianceFrame.pack(side="left", expand=True, fill="both")

  def displayI2CSetupPage(self):
    self.i2cSetupFrame = I2CSetupFrame(self.mainContentFrame)
    self.i2cSetupFrame.pack(side="left", expand=True, fill="both")

  def displayResetPage(self):
    self.resetFrame = ResetSetupFrame(self.mainContentFrame)
    self.resetFrame.pack(side="left", expand=True, fill="both")