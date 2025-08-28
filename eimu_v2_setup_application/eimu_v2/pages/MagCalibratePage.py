import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy import linalg
import time
from termcolor import colored

from eimu_v2.globalParams import g



class MagCalibrateFrame(tb.Frame):
  def __init__(self, parentFrame):
    super().__init__(master=parentFrame)

    self.b = np.zeros([3, 1])
    self.A_1 = np.eye(3)
    self.F = 1

    self.magArray = []
    self.mag_x = []
    self.mag_y = []
    self.mag_z = []

    g.eimuV2.setWorldFrameId(1)

    self.anim = None
    self.stop = False
    self.calibrated = False
    self.HISTORY_SIZE = 10000

    self.fig, self.ax = None, None
    

    self.label = tb.Label(self, text="CALIBRATE MAGNETOMETER SENSOR", font=('Monospace',16, 'bold') ,bootstyle="dark")
    self.frame = tb.Frame(self)
    
    #create widgets to be added to frame1
    buttonStyle = tb.Style()
    buttonStyleName = 'primary.TButton'
    buttonStyle.configure(buttonStyleName, font=('Monospace',10,'bold'))
    self.calMagButton = tb.Button(self.frame, text="START",
                               style=buttonStyleName, padding=20,
                               command=self.runCalibration)
    
    #add framed widgets to frame
    self.calMagButton.pack(side='top', expand=True, fill="both")

    #add label and frame to CalibrateAccFrame
    self.label.pack(side='top', pady=(20,50))
    self.frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.3)


  def calibrate(self):
      
    # ellipsoid fit
    s = np.array(self.magArray).T
    M, n, d = self.__ellipsoid_fit(s)
    
    # calibration parameters
    # note: some implementations of sqrtm return complex type, taking real
    M_1 = linalg.inv(M)
    self.b = -np.dot(M_1, n)
    self.A_1 = np.real(self.F / np.sqrt(np.dot(n.T, np.dot(M_1, n)) - d) * linalg.sqrtm(M))

    ################################################
    b_vect = np.zeros([3, 1])
    A_mat = np.eye(3)

    g.eimuV2.writeMagHardOffset(0, self.b[0][0])
    g.eimuV2.writeMagHardOffset(1, self.b[1][0])
    g.eimuV2.writeMagHardOffset(2, self.b[2][0])

    b_vect[0][0] = g.eimuV2.readMagHardOffset(0)
    b_vect[1][0] = g.eimuV2.readMagHardOffset(1)
    b_vect[2][0] = g.eimuV2.readMagHardOffset(2)

    
    g.eimuV2.writeMagSoftOffset0(0, self.A_1[0][0])
    g.eimuV2.writeMagSoftOffset0(1, self.A_1[0][1])
    g.eimuV2.writeMagSoftOffset0(2, self.A_1[0][2])

    g.eimuV2.writeMagSoftOffset1(0, self.A_1[1][0])
    g.eimuV2.writeMagSoftOffset1(1, self.A_1[1][1])
    g.eimuV2.writeMagSoftOffset1(2, self.A_1[1][2])

    g.eimuV2.writeMagSoftOffset2(0, self.A_1[2][0])
    g.eimuV2.writeMagSoftOffset2(1, self.A_1[2][1])
    g.eimuV2.writeMagSoftOffset2(2, self.A_1[2][2])

    A_mat[0][0] = g.eimuV2.readMagSoftOffset0(0)
    A_mat[0][1] = g.eimuV2.readMagSoftOffset0(1)
    A_mat[0][2] = g.eimuV2.readMagSoftOffset0(2)

    A_mat[1][0] = g.eimuV2.readMagSoftOffset1(0)
    A_mat[1][1] = g.eimuV2.readMagSoftOffset1(1)
    A_mat[1][2] = g.eimuV2.readMagSoftOffset1(2)

    A_mat[2][0] = g.eimuV2.readMagSoftOffset2(0)
    A_mat[2][1] = g.eimuV2.readMagSoftOffset2(1)
    A_mat[2][2] = g.eimuV2.readMagSoftOffset2(2)

    ################################################
    
    print(colored("\nHard Iron Offset (b_vect)", 'green'))
    print(b_vect)
    
    print(colored("\nSoft Iron Offset (A_mat):", 'green'))
    print(A_mat)




  def __ellipsoid_fit(self, s):
    ''' Estimate ellipsoid parameters from a set of points.

      Parameters
      ----------
      s : array_like
        The samples (M,N) where M=3 (x,y,z) and N=number of samples.

      Returns
      -------
      M, n, d : array_like, array_like, float
        The ellipsoid parameters M, n, d.

      References
      ----------
      .. [1] Qingde Li; Griffiths, J.G., "Least squares ellipsoid specific
          fitting," in Geometric Modeling and Processing, 2004.
          Proceedings, vol., no., pp.335-340, 2004
    '''

    # D (samples)
    D = np.array([s[0]**2., s[1]**2., s[2]**2.,
                  2.*s[1]*s[2], 2.*s[0]*s[2], 2.*s[0]*s[1],
                  2.*s[0], 2.*s[1], 2.*s[2], np.ones_like(s[0])])

    # S, S_11, S_12, S_21, S_22 (eq. 11)
    S = np.dot(D, D.T)
    S_11 = S[:6,:6]
    S_12 = S[:6,6:]
    S_21 = S[6:,:6]
    S_22 = S[6:,6:]

    # C (Eq. 8, k=4)
    C = np.array([[-1,  1,  1,  0,  0,  0],
                  [ 1, -1,  1,  0,  0,  0],
                  [ 1,  1, -1,  0,  0,  0],
                  [ 0,  0,  0, -4,  0,  0],
                  [ 0,  0,  0,  0, -4,  0],
                  [ 0,  0,  0,  0,  0, -4]])

    # v_1 (eq. 15, solution)
    E = np.dot(linalg.inv(C),
                S_11 - np.dot(S_12, np.dot(linalg.inv(S_22), S_21)))

    E_w, E_v = np.linalg.eig(E)

    v_1 = E_v[:, np.argmax(E_w)]
    if v_1[0] < 0: v_1 = -v_1

    # v_2 (eq. 13, solution)
    v_2 = np.dot(np.dot(-np.linalg.inv(S_22), S_21), v_1)

    # quadric-form parameters
    M = np.array([[v_1[0], v_1[3], v_1[4]],
                  [v_1[3], v_1[1], v_1[5]],
                  [v_1[4], v_1[5], v_1[2]]])
    n = np.array([[v_2[0]],
                  [v_2[1]],
                  [v_2[2]]])
    d = v_2[3]

    return M, n, d



  def onClick(self,event):   
    if self.stop == False:
      self.anim.event_source.stop()
      if self.calibrated == False:
        self.calibrate()
        self.mag_x = []
        self.mag_y = []
        self.mag_z = []
        self.magArray = []
        self.calibrated = True
      self.stop = True
    else:
      self.anim.event_source.start()
      self.stop = False

  def onClose(self,event): 
    plt.close()
    self.b = np.zeros([3, 1])
    self.A_1 = np.eye(3)
    self.F = 1

    self.magArray = []
    self.mag_x = []
    self.mag_y = []
    self.mag_z = []

    self.anim = None
    self.stop = False
    self.calibrated = False
    self.HISTORY_SIZE = 10000

    self.fig, self.ax = None, None 

      
  def animate(self,i):
    try:
      if self.calibrated == False:
        mx = g.eimuV2.readMagRaw(0)
        my = g.eimuV2.readMagRaw(1)
        mz = g.eimuV2.readMagRaw(2)
      else:
        mx = g.eimuV2.readMag(0)
        my = g.eimuV2.readMag(1)
        mz = g.eimuV2.readMag(2)
      
      self.magArray.append([mx,my,mz])
      self.mag_x.append(mx)
      self.mag_y.append(my)
      self.mag_z.append(mz)

      # Clear all axis
      self.ax.cla()

      # Display the sub-plots
      self.ax.scatter(self.mag_x, self.mag_y, color='r')
      self.ax.scatter(self.mag_y, self.mag_z, color='g')
      self.ax.scatter(self.mag_z, self.mag_x, color='b')
      
      if len(self.mag_x) == self.HISTORY_SIZE:
        self.anim.event_source.stop()
    except:
      pass
    

  def runCalibration(self):
    self.fig, self.ax = plt.subplots(1, 1)
    self.ax.set_aspect(1)

    self.fig.canvas.mpl_connect('close_event', self.onClose)
    self.fig.canvas.mpl_connect('button_press_event', self.onClick)    
    self.anim = FuncAnimation(self.fig, self.animate, frames = np.arange(0, 10000, 1), interval=50)
    plt.show()